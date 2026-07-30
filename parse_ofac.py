import re, json, os, sys, subprocess, html

URL = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ENHANCED_XML"
OUT = "vessels.json"

def dec(v):
    """Decode XML/HTML entities (&amp; &lt; etc.) captured verbatim by the regex parser."""
    return html.unescape(v) if isinstance(v, str) else v


# ── Download ──────────────────────────────────────────────────────────────────
print("Downloading SDN Enhanced XML (this takes 60-90 seconds, file is ~108MB)...")
result = subprocess.run(
    ["curl", "-L", "--retry", "3", "--retry-delay", "5",
     "--connect-timeout", "30", "--max-time", "300",
     "-o", "sdn.xml", URL],
    capture_output=True, text=True
)
if result.returncode != 0:
    print("ERROR: curl failed:")
    print(result.stderr)
    sys.exit(1)

size = os.path.getsize("sdn.xml")
print(f"Downloaded: {size:,} bytes")
if size < 1_000_000:
    print("ERROR: file too small — download may have failed. Contents:")
    with open("sdn.xml") as f:
        print(f.read(2000))
    sys.exit(1)

# ── Parse ─────────────────────────────────────────────────────────────────────
print("Reading file...")
with open("sdn.xml", "r", encoding="utf-8") as f:
    content = f.read()
print(f"File size: {len(content):,} chars")

entity_pattern = re.compile(r'<entity id="(\d+)">(.*?)</entity>', re.DOTALL)

vessels = []
total = 0
for m in entity_pattern.finditer(content):
    total += 1
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
                    primary_name = dec(nm)
                else:
                    aliases.append(dec(nm))

    features = {}
    fb = re.search(r'<features>(.*?)</features>', body, re.DOTALL)
    if fb:
        for fe in re.findall(r'<feature id="[^"]+">(.*?)</feature>', fb.group(1), re.DOTALL):
            ft = re.search(r'<type[^>]*>([^<]+)</type>', fe)
            fv = re.search(r'<value>([^<]+)</value>', fe)
            if ft and fv:
                features[ft.group(1).strip()] = dec(fv.group(1).strip())

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

print(f"Total entities scanned: {total:,}")
print(f"Vessel entities found:  {len(vessels):,}")
print(f"Vessels with IMO:       {sum(1 for v in vessels if v['imo']):,}")

# ── Write output ──────────────────────────────────────────────────────────────
with open(OUT, "w") as f:
    json.dump(vessels, f)

out_size = os.path.getsize(OUT)
print(f"Written {OUT} ({out_size:,} bytes)")

os.remove("sdn.xml")
print("Cleaned up. Done.")
