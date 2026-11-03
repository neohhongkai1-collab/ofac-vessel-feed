Step 1 - Download the 108MB XML from the US Treasury 

The first step is to go directly to the source. The US Treasury's Office of Foreign Assets Control publishes the SDN Enhanced XML at their official Sanctions List Service portal. This is the only fully authoritative version of the list. It contains third-party databases, aggregators and commercial services all ultimately derive their data from this same file. By downloading directly from the Treasury, we guarantee that our data is as accurate and complete as it is the official list so there is no middleman introducing delays or inaccuracies. 

 

Step 2 - Identify All Vessel Entities 

The SDN list contains 19,254 designated entities in total like individuals, companies and vessels that are all mixed together in one file. The XML assigns each entity a type code, with code 602 specifically designating vessels. We extract exactly the 1,517 vessels. 

 

Step 3 — Extract the IMO Number as the Primary Identifier  

Of all the fields in a vessel's record, the IMO number is the most important. The International Maritime Organization assigns each vessel a permanent seven-digit number at the time of construction. It stays with the vessel forever, regardless of name changes, flag changes or ownership transfers. Sanctioned vessels routinely rename themselves and reflag to different countries to evade detection. Matching by vessel name alone would miss these cases entirely. By anchoring every record to its IMO number, we ensure the vessel is correctly identified even if it has been renamed ten times since its designation. The IMO number is extracted from the vessel's identity documents block within the XML, where it is stored in the format "IMO XXXXXXX"  

 

Step 4 — Extract Vessel Features  

Beyond the IMO number, the XML contains a features block for each vessel recording its flag state, call sign, vessel type, owner, gross tonnage and year of build. These fields are extracted because they serve two purposes. First, they populate the vessel profile displayed in VesselScreen, giving users enough context to verify they are looking at the correct vessel. Second, the owner fieldcreates a direct connection between the vessel screening and the company screening. If the OFAC record names an owner, that name can be cross-referenced during company screening without needing a separate lookup.  

 

Step 5 — Extract All Sanctions Programmes 

Each vessel on the SDN list is designated under one or more specific sanctions programmes. For example IRAN-EO13902 (Iran oil sector), RUSSIA-EO14024 (Russia-related), UKRAINE-EO13662 or CUBA. These programme codes matter because they tell you the nature and jurisdiction of the risk. A vessel sanctioned under an Iran programme carries very different legal implications for a Singapore bunker trader than one sanctioned under a Russia programme. By capturing every programme a vessel falls under, VesselScreen can display the full sanctions picture rather than simply flagging a vessel as "sanctioned" without context. 

 

Because not every sanctions programme affects every company equally. Different countries and jurisdictions enforce different programmes. If a vessel is sanctioned under an Iran programme, that is a hard stop for almost any company doing international trade. US, UK, EU, and Singapore banks will all refuse to process payments linked to it. But if a vessel is sanctioned under a Russia programme, the legal implications depend on who you are dealing with and which jurisdiction your bank operates under.  

 

In short, knowing a vessel is "sanctioned" is not enough on its own. You need to know why it is sanctioned and under whose rules because that determines what your actual legal exposure is and what you need to tell your bank.  
