import re, json, urllib.request, os

URL = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ENHANCED_XML"
OUT = "vessels.json"

print("Downloading SDN Enhanced XML...")
urllib.request.urlretrieve(URL, "sdn.xml")
print("Download complete.")

with open("sdn.xml", "r", encoding="utf-8") as f:
    content = f.read()

print(f"File size: {len(content):,} chars — Parsing vessels...")

entity_pattern = re.compile(r'<entity id="(\d+)">(.*?)</entity>', re.DOTALL)

vessels = []
for m in entity_pattern.finditer(content):
    body = m.group(2)
    if '<entityType refId="602">Vessel</entityType>' not in body:
        continue

    programs = re.findall(r'<sanctionsProgram[^>]*>([^<]+)</sanctionsProgram>', body)

    names_block = re.search(r'<names>(.*?)</names>', body, re.DOTALL)
    primary_name, aliases = '', []
    if names_block:
        for ne in re.findall(r'<name id="[^"]+">(.*?)</name>', names_block.group(1), re.DOTALL):
            fn = re.search(r'<formattedFullName>([^<]+)</formattedFullName>', ne)
            if fn:
                nm = fn.group(1).strip()
                if '<isPrimary>true</isPrimary>' in ne:
                    primary_name = nm
                else:
                    aliases.append(nm)

    features = {}
    fb = re.search(r'<features>(.*?)</features>', body, re.DOTALL)
    if fb:
        for fe in re.findall(r'<feature id="[^"]+">(.*?)</feature>', fb.group(1), re.DOTALL):
            ft = re.search(r'<type[^>]*>([^<]+)</type>', fe)
            fv = re.search(r'<value>([^<]+)</value>', fe)
            if ft and fv:
                features[ft.group(1).strip()] = fv.group(1).strip()

    imo = ''
    idb = re.search(r'<identityDocuments>(.*?)</identityDocuments>', body, re.DOTALL)
    if idb:
        for ide in re.findall(r'<identityDocument id="[^"]+">(.*?)</identityDocument>', idb.group(1), re.DOTALL):
            if 'Vessel Registration Identification' in ide:
                dn = re.search(r'<documentNumber>([^<]+)</documentNumber>', ide)
                if dn:
                    imo = re.sub(r'(?i)^imo\s*', '', dn.group(1).strip())

    vessels.append({
        "imo":         imo,
        "name":        primary_name,
        "aliases":     aliases,
        "programs":    programs,
        "flag":        features.get("Vessel Flag", ""),
        "call_sign":   features.get("Vessel Call Sign", ""),
        "vessel_type": features.get("VESSEL TYPE", ""),
        "owner":       features.get("Vessel Owner", ""),
        "tonnage":     features.get("Vessel Tonnage", features.get("Vessel Gross Registered Tonnage", "")),
        "year_build":  features.get("Vessel Year of Build", ""),
    })

with open(OUT, "w") as f:
    json.dump(vessels, f)

print(f"Done — {len(vessels)} vessels written to {OUT}")
os.remove("sdn.xml")
print("Cleaned up sdn.xml")
