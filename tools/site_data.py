"""Content data for sdtt.de — edit here, then run `python tools/build.py`.

PLATZHALTER: every name, phone number, project, budget and figure below is
sample data from the spec. Replace with verified company data before go-live.
"""

SITE_URL = "https://www.sdtt.de"

# Set to True once real content is in place — until then pages carry
# <meta name="robots" content="noindex"> so placeholder data is never indexed.
INDEXABLE = False

COMPANY = {
    "name": "SDTT GmbH",
    "street": "Wilhelmstraße 45",
    "zip_city": "70182 Stuttgart",
    "country": {"de": "Deutschland", "en": "Germany"},
    "email": "info@sdtt.de",
    "phone": ("+49 711 0000-1000", "+4971100001000"),
    "emergency": ("+49 711 0000-1099", "+4971100001099"),
    "whatsapp": ("+49 170 0000000", "491700000000"),
    "hours": {"de": "Mo–Fr 7:30–17:00 Uhr", "en": "Mon–Fri 7:30 am – 5:00 pm"},
    "founded_years": "20+",
}

# Key figures (spec section 10) — PLATZHALTER, verify before go-live.
FIGURES = [
    ("20+", {"de": "Jahre Erfahrung mit öffentlichen Auftraggebern", "en": "years of experience with public clients"}),
    ("120+", {"de": "abgeschlossene öffentliche Projekte", "en": "completed public projects"}),
    ("15", {"de": "Kommunen als Auftraggeber in Baden-Württemberg", "en": "municipalities as clients in Baden-Württemberg"}),
    ("90+", {"de": "fest angestellte Mitarbeitende", "en": "permanent employees"}),
]

CATEGORIES = [
    {
        "key": "education", "icon": "education",
        "label": {"de": "Bildungseinrichtungen", "en": "Educational facilities"},
        "desc": {"de": "Schulen, Kindertagesstätten, Bibliotheken", "en": "Schools, day-care centres, libraries"},
    },
    {
        "key": "health", "icon": "health",
        "label": {"de": "Gesundheitseinrichtungen", "en": "Healthcare facilities"},
        "desc": {"de": "Krankenhäuser, Kliniken, Gesundheitszentren", "en": "Hospitals, clinics, health centres"},
    },
    {
        "key": "administration", "icon": "landmark",
        "label": {"de": "Verwaltung und Soziales", "en": "Administration and social"},
        "desc": {"de": "Rathäuser, Verwaltungsgebäude, Sozialzentren", "en": "Town halls, administrative buildings, social centres"},
    },
    {
        "key": "culture", "icon": "culture",
        "label": {"de": "Kultur und Gemeinwesen", "en": "Culture and community"},
        "desc": {"de": "Museen, Kulturzentren, Stadtbibliotheken", "en": "Museums, cultural centres, city libraries"},
    },
    {
        "key": "infrastructure", "icon": "infrastructure",
        "label": {"de": "Infrastruktur und Versorgung", "en": "Infrastructure and utilities"},
        "desc": {"de": "Feuerwehr, Wasserversorgung, Bauhöfe", "en": "Fire stations, water supply, municipal depots"},
    },
]

SIZES = {
    "compact": {"de": "Kompakt (bis 1 Mio. €)", "en": "Compact (up to €1 m)"},
    "medium": {"de": "Mittel (1–2,5 Mio. €)", "en": "Medium (€1–2.5 m)"},
    "large": {"de": "Groß (über 2,5 Mio. €)", "en": "Large (over €2.5 m)"},
}

# People for tender / technical / quality contacts (spec 4.5) — PLATZHALTER.
PEOPLE = [
    {
        "key": "tenders",
        "role": {"de": "Öffentliche Ausschreibungen", "en": "Public procurement"},
        "role_de": "Ausschreibungsbetreuer",
        "name": "Dipl.-Ing. Michael Forster",
        "email": "ausschreibungen@sdtt.de",
        "phone": ("+49 711 0000-1010", "+4971100001010"),
        "office": "Wilhelmstraße 45, 70182 Stuttgart",
        "focus": None,
        "fn": {
            "de": "Koordiniert alle öffentlichen Ausschreibungen, Angebote und Eignungsnachweise sowie die Abstimmung mit Vergabestellen und Behörden.",
            "en": "Coordinates all public tenders, bids and proof-of-eligibility documents, and liaises with contracting authorities.",
        },
    },
    {
        "key": "technical",
        "role": {"de": "Technische Leitung", "en": "Technical department"},
        "role_de": "Technischer Leiter",
        "name": "Dipl.-Ing. (FH) Thomas Bergmann",
        "email": "technik@sdtt.de",
        "phone": ("+49 711 0000-1020", "+4971100001020"),
        "office": None,
        "focus": {"de": "Großsanierungen von 0,5 bis 5 Mio. €", "en": "Major refurbishments from €0.5 m to €5 m"},
        "fn": {
            "de": "Verantwortet die technische Projektprüfung und die Ausführungsqualität und stellt die Einhaltung von DIN und VOB sicher.",
            "en": "Responsible for technical project review and execution quality, and ensures compliance with DIN and VOB.",
        },
    },
    {
        "key": "quality",
        "role": {"de": "Qualitätsmanagement", "en": "Quality management"},
        "role_de": "Qualitätsleiterin",
        "name": "Dr. Sabine Hoffmann",
        "email": "qualitaet@sdtt.de",
        "phone": ("+49 711 0000-1030", "+4971100001030"),
        "office": None,
        "focus": None,
        "fn": {
            "de": "Steuert die Qualitätskontrolle, externe Audits durch TÜV und DEKRA sowie die Abnahme der Leistungen.",
            "en": "Manages quality control, external audits by TÜV and DEKRA, and the acceptance of works.",
        },
    },
]

# Seven downloadable documents (spec 4.6). Files are generated as placeholders.
DOCS = [
    {
        "key": "archive",
        "file": {"de": "projektarchiv.pdf", "en": "project-archive.pdf"},
        "title": {"de": "Projektarchiv – alle Referenzprojekte", "en": "Project archive – all reference projects"},
        "note": {"de": "Übersicht aller abgeschlossenen öffentlichen Projekte", "en": "Overview of all completed public projects"},
    },
    {
        "key": "certificates",
        "file": {"de": "zertifikate-iso-9001-vob-din.pdf", "en": "certificates-iso-9001-vob-din.pdf"},
        "title": {"de": "Zertifikate ISO 9001, VOB/DIN", "en": "Certificates ISO 9001, VOB/DIN"},
        "note": {"de": "Zertifikate und Konformitätsnachweise", "en": "Certificates and proof of conformity"},
    },
    {
        "key": "references",
        "file": {"de": "referenzschreiben.pdf", "en": "reference-letters.pdf"},
        "title": {"de": "Referenzschreiben", "en": "Reference letters"},
        "note": {"de": "von Kommunen und öffentlichen Auftraggebern", "en": "from municipalities and public clients"},
    },
    {
        "key": "cvs",
        "file": {"de": "lebenslaeufe-bauleitung.pdf", "en": "cvs-site-management.pdf"},
        "title": {"de": "Lebensläufe Bauleitung und Ingenieure", "en": "CVs of site managers and engineers"},
        "note": {"de": "Qualifikationen des Schlüsselpersonals", "en": "Qualifications of key personnel"},
    },
    {
        "key": "methodology",
        "file": {"de": "projektmanagement-methodik.pdf", "en": "project-management-methodology.pdf"},
        "title": {"de": "Projektmanagement-Methodik", "en": "Project management methodology"},
        "note": {"de": "Prozesse nach VOB/B und DIN", "en": "Processes according to VOB/B and DIN"},
    },
    {
        "key": "warranty",
        "file": {"de": "gewaehrleistungsbedingungen.pdf", "en": "warranty-terms.pdf"},
        "title": {"de": "Gewährleistungsbedingungen", "en": "Warranty terms"},
        "note": {"de": "nach § 634a BGB", "en": "according to § 634a BGB"},
    },
    {
        "key": "insurance",
        "file": {"de": "versicherung-und-buergschaften.pdf", "en": "insurance-and-guarantees.pdf"},
        "title": {"de": "Versicherungsnachweis und Bürgschaften", "en": "Proof of insurance and guarantees"},
        "note": {"de": "Betriebshaftpflicht, Bauleistungsversicherung, Bürgschaftsrahmen", "en": "Liability insurance, contractor's all-risk insurance, guarantee facility"},
    },
]

# Projects — the first three come from the spec, the rest are samples.
# PLATZHALTER: replace with the verified project archive.
PROJECTS = [
    {
        "slug": "eichendorff-gymnasium-stuttgart",
        "featured": True, "sample": False,
        "type": "education", "city": "Stuttgart", "size": "large", "start": 2023, "end": 2024,
        "floors": 4, "seed": 3,
        "title": {"de": "Eichendorff-Gymnasium Stuttgart", "en": "Eichendorff-Gymnasium, Stuttgart"},
        "client": {"de": "Landeshauptstadt Stuttgart, Schulverwaltungsamt", "en": "City of Stuttgart, School Administration Office"},
        "budget": {"de": "ca. 3,8 Mio. € netto", "en": "approx. €3.8 m net"},
        "duration": {"de": "14 Monate, drei Bauabschnitte", "en": "14 months, three construction phases"},
        "team": {"de": "Bauleiter, 2 Poliere, bis zu 38 eigene Fachkräfte", "en": "Site manager, 2 foremen, up to 38 in-house specialists"},
        "summary": {
            "de": "Generalsanierung eines Schulgebäudes aus den 1970er-Jahren im laufenden Unterrichtsbetrieb.",
            "en": "Complete refurbishment of a 1970s school building while classes continued.",
        },
        "scope": {
            "de": ["Generalsanierung im laufenden Schulbetrieb", "Wärmedämmverbundsystem an der gesamten Fassade", "Austausch von 214 Fenstern", "Neue Lüftungs- und Heizungstechnik"],
            "en": ["Complete refurbishment while the school remained in use", "External thermal insulation composite system on the entire facade", "Replacement of 214 windows", "New ventilation and heating systems"],
        },
        "text": {
            "de": [
                "Das Gymnasium wurde in drei Bauabschnitten saniert, sodass der Unterricht ohne Unterbrechung weiterlaufen konnte. Lärmintensive Arbeiten wurden mit der Schulleitung in die Ferienzeiten und Nachmittage gelegt.",
                "Die energetische Sanierung erfolgt nach den Anforderungen des Gebäudeenergiegesetzes (GEG). Der Auftraggeber erhielt wöchentliche Baufortschritts- und Kostenberichte sowie eine vollständige Bestandsdokumentation zur Abnahme.",
            ],
            "en": [
                "The school was refurbished in three construction phases so that teaching could continue without interruption. Noisy work was scheduled with the school management during holidays and afternoons.",
                "The energy refurbishment meets the requirements of the German Buildings Energy Act (GEG). The client received weekly progress and cost reports and complete as-built documentation at acceptance.",
            ],
        },
        "certs": ["VOB/B", "DIN", "GEG", "ISO 9001"],
        "contact": {"name": "Herr Klaus Müller", "email": "k.mueller@stuttgart.example", "phone": ("+49 711 0000-2000", "+4971100002000")},
    },
    {
        "slug": "theodor-heuss-haus-ludwigsburg",
        "featured": True, "sample": False,
        "type": "administration", "city": "Ludwigsburg", "size": "medium", "start": 2022, "end": 2023,
        "floors": 3, "seed": 5,
        "title": {"de": "Sozialzentrum Theodor-Heuss-Haus, Ludwigsburg", "en": "Theodor-Heuss-Haus social centre, Ludwigsburg"},
        "client": {"de": "Stadt Ludwigsburg, Fachbereich Bürgerschaftliches Engagement und Soziales", "en": "City of Ludwigsburg, Department of Civic Engagement and Social Affairs"},
        "budget": {"de": "ca. 2,1 Mio. € netto", "en": "approx. €2.1 m net"},
        "duration": {"de": "11 Monate", "en": "11 months"},
        "team": {"de": "Bauleiterin, Polier, bis zu 24 eigene Fachkräfte", "en": "Site manager, foreman, up to 24 in-house specialists"},
        "summary": {
            "de": "Umbau und energetische Sanierung eines Sozialzentrums mit vollständiger Barrierefreiheit.",
            "en": "Conversion and energy refurbishment of a social centre with full accessibility.",
        },
        "scope": {
            "de": ["Barrierefreier Umbau nach DIN 18040-1 inklusive Aufzug", "Brandschutzertüchtigung und neue Fluchtwege", "Dämmung von Dach und oberster Geschossdecke", "Erneuerung der Sanitär- und Elektroinstallation"],
            "en": ["Accessible conversion to DIN 18040-1 including a lift", "Fire protection upgrade and new escape routes", "Insulation of the roof and top-floor ceiling", "New sanitary and electrical installations"],
        },
        "text": {
            "de": [
                "Das Theodor-Heuss-Haus wurde während der Bauzeit teilweise weiter genutzt. Beratungsangebote zogen abschnittsweise in bereits fertiggestellte Bereiche um.",
                "Schwerpunkte waren Barrierefreiheit und Brandschutz. Alle Nachträge wurden vor Ausführung schriftlich vom Auftraggeber freigegeben.",
            ],
            "en": [
                "The Theodor-Heuss-Haus remained partly in use during construction. Counselling services moved section by section into areas that were already finished.",
                "The focus was on accessibility and fire protection. All change orders were approved in writing by the client before execution.",
            ],
        },
        "certs": ["VOB/B", "DIN 18040", "GEG", "ISO 9001"],
        "contact": {"name": "Frau Andrea Weber", "email": "a.weber@ludwigsburg.example", "phone": ("+49 7141 0000-300", "+49714100003000")},
    },
    {
        "slug": "feuerwehr-esslingen",
        "featured": True, "sample": False,
        "type": "infrastructure", "city": "Esslingen am Neckar", "size": "large", "start": 2023, "end": 2025,
        "floors": 2, "seed": 7,
        "title": {"de": "Feuerwache Esslingen am Neckar", "en": "Fire station, Esslingen am Neckar"},
        "client": {"de": "Stadt Esslingen am Neckar, Feuerwehr", "en": "City of Esslingen am Neckar, Fire Department"},
        "budget": {"de": "ca. 4,6 Mio. € netto", "en": "approx. €4.6 m net"},
        "duration": {"de": "20 Monate bei laufendem Einsatzbetrieb", "en": "20 months while the station remained operational"},
        "team": {"de": "Bauleiter, 2 Poliere, bis zu 42 eigene Fachkräfte", "en": "Site manager, 2 foremen, up to 42 in-house specialists"},
        "summary": {
            "de": "Erweiterung und Sanierung einer Feuerwache, ohne den 24/7-Einsatzbetrieb einzuschränken.",
            "en": "Extension and refurbishment of a fire station without restricting 24/7 emergency operations.",
        },
        "scope": {
            "de": ["Erweiterung der Fahrzeughalle um vier Stellplätze", "Sanierung des Sozial- und Umkleidetrakts nach Schwarz-Weiß-Prinzip", "Abgasabsaugung für alle Stellplätze", "Photovoltaikanlage auf dem Hallendach"],
            "en": ["Extension of the vehicle hall by four bays", "Refurbishment of the staff and changing area with separate clean and contaminated zones", "Vehicle exhaust extraction for all bays", "Photovoltaic system on the hall roof"],
        },
        "text": {
            "de": [
                "Die Ausrückwege der Feuerwehr mussten während der gesamten Bauzeit frei bleiben. Die Baustellenlogistik wurde dafür mit der Wachleitung abgestimmt und täglich überprüft.",
                "Die Abnahme erfolgte mit Begleitung durch einen unabhängigen Sachverständigen. Fertigstellung termingerecht und im Rahmen des Budgets.",
            ],
            "en": [
                "The fire brigade's exit routes had to remain clear throughout construction. Site logistics were agreed with the station management and checked daily.",
                "Acceptance took place with an independent expert present. The project was completed on schedule and within budget.",
            ],
        },
        "certs": ["VOB/B", "DIN", "GEG", "ISO 9001"],
        "contact": {"name": "Herr Stefan Krämer", "email": "s.kraemer@esslingen.example", "phone": ("+49 711 0000-3000", "+4971100003000")},
    },
    # ---- Sample projects (Musterdaten) ----
    {
        "slug": "kita-sonnenhof-boeblingen", "featured": False, "sample": True,
        "type": "education", "city": "Böblingen", "size": "compact", "start": 2024, "end": 2024, "floors": 2, "seed": 11,
        "title": {"de": "Kindertagesstätte Sonnenhof, Böblingen", "en": "Sonnenhof day-care centre, Böblingen"},
        "client": {"de": "Stadt Böblingen, Amt für Jugend, Schule und Sport", "en": "City of Böblingen, Youth, Schools and Sport Office"},
        "budget": {"de": "ca. 0,8 Mio. € netto", "en": "approx. €0.8 m net"},
        "duration": {"de": "6 Monate", "en": "6 months"},
        "team": {"de": "Bauleiter, Polier, bis zu 14 Fachkräfte", "en": "Site manager, foreman, up to 14 specialists"},
        "summary": {"de": "Sanierung und Erweiterung um eine Krippengruppe.", "en": "Refurbishment and extension by one nursery group."},
        "scope": {"de": ["Anbau in Holzbauweise für eine Krippengruppe", "Neue Fenster und Sonnenschutz", "Sanierung der Sanitärräume"], "en": ["Timber-frame extension for a nursery group", "New windows and solar shading", "Refurbishment of the washrooms"]},
        "certs": ["VOB/B", "GEG"],
    },
    {
        "slug": "grundschule-am-park-waiblingen", "featured": False, "sample": True,
        "type": "education", "city": "Waiblingen", "size": "medium", "start": 2022, "end": 2023, "floors": 3, "seed": 13,
        "title": {"de": "Grundschule am Park, Waiblingen", "en": "Grundschule am Park, Waiblingen"},
        "client": {"de": "Stadt Waiblingen, Hochbauamt", "en": "City of Waiblingen, Building Construction Office"},
        "budget": {"de": "ca. 1,6 Mio. € netto", "en": "approx. €1.6 m net"},
        "duration": {"de": "9 Monate", "en": "9 months"},
        "team": {"de": "Bauleiter, Polier, bis zu 20 Fachkräfte", "en": "Site manager, foreman, up to 20 specialists"},
        "summary": {"de": "Energetische Sanierung und Brandschutzertüchtigung.", "en": "Energy refurbishment and fire protection upgrade."},
        "scope": {"de": ["Fassadendämmung und Fenstertausch", "Zweiter baulicher Rettungsweg", "LED-Beleuchtung in allen Klassenräumen"], "en": ["Facade insulation and window replacement", "Second structural escape route", "LED lighting in all classrooms"]},
        "certs": ["VOB/B", "GEG", "ISO 9001"],
    },
    {
        "slug": "klinikum-sindelfingen-pflegestation", "featured": False, "sample": True,
        "type": "health", "city": "Sindelfingen", "size": "large", "start": 2023, "end": 2024, "floors": 4, "seed": 17,
        "title": {"de": "Kreisklinik Sindelfingen, Sanierung Pflegestation", "en": "District hospital Sindelfingen, ward refurbishment"},
        "client": {"de": "Kommunaler Klinikträger, Landkreis Böblingen", "en": "Municipal hospital operator, Böblingen district"},
        "budget": {"de": "ca. 3,2 Mio. € netto", "en": "approx. €3.2 m net"},
        "duration": {"de": "12 Monate im laufenden Klinikbetrieb", "en": "12 months while the hospital remained in operation"},
        "team": {"de": "Bauleiter, 2 Poliere, bis zu 30 Fachkräfte", "en": "Site manager, 2 foremen, up to 30 specialists"},
        "summary": {"de": "Kernsanierung einer Pflegestation mit 32 Betten.", "en": "Full refurbishment of a 32-bed ward."},
        "scope": {"de": ["Staubschutz- und Hygienekonzept für den laufenden Betrieb", "Neue Patientenbäder", "Medizinische Gasversorgung und Elektrotechnik"], "en": ["Dust protection and hygiene concept for continued operation", "New patient bathrooms", "Medical gas supply and electrical systems"]},
        "certs": ["VOB/B", "DIN", "ISO 9001"],
    },
    {
        "slug": "gesundheitszentrum-fellbach", "featured": False, "sample": True,
        "type": "health", "city": "Fellbach", "size": "medium", "start": 2021, "end": 2022, "floors": 3, "seed": 19,
        "title": {"de": "Gesundheitszentrum Fellbach", "en": "Fellbach health centre"},
        "client": {"de": "Stadt Fellbach, Gebäudemanagement", "en": "City of Fellbach, Facility Management"},
        "budget": {"de": "ca. 1,9 Mio. € netto", "en": "approx. €1.9 m net"},
        "duration": {"de": "10 Monate", "en": "10 months"},
        "team": {"de": "Bauleiter, Polier, bis zu 22 Fachkräfte", "en": "Site manager, foreman, up to 22 specialists"},
        "summary": {"de": "Umbau eines Bestandsgebäudes zu einem Gesundheitszentrum.", "en": "Conversion of an existing building into a health centre."},
        "scope": {"de": ["Umbau für fünf Praxiseinheiten", "Barrierefreier Zugang und Aufzug", "Neue Haustechnik"], "en": ["Conversion for five medical practice units", "Step-free access and lift", "New building services"]},
        "certs": ["VOB/B", "DIN 18040", "GEG"],
    },
    {
        "slug": "rathaus-kornwestheim", "featured": False, "sample": True,
        "type": "administration", "city": "Kornwestheim", "size": "medium", "start": 2022, "end": 2022, "floors": 3, "seed": 23,
        "title": {"de": "Rathaus Kornwestheim", "en": "Kornwestheim town hall"},
        "client": {"de": "Stadt Kornwestheim, Fachbereich Hochbau", "en": "City of Kornwestheim, Building Construction Department"},
        "budget": {"de": "ca. 1,2 Mio. € netto", "en": "approx. €1.2 m net"},
        "duration": {"de": "7 Monate", "en": "7 months"},
        "team": {"de": "Bauleiter, Polier, bis zu 16 Fachkräfte", "en": "Site manager, foreman, up to 16 specialists"},
        "summary": {"de": "Dach- und Fenstersanierung bei laufendem Verwaltungsbetrieb.", "en": "Roof and window refurbishment while administration continued."},
        "scope": {"de": ["Neueindeckung und Dämmung des Daches", "Austausch der Fenster unter Denkmalschutzauflagen", "Blitzschutzanlage"], "en": ["New roof covering and insulation", "Window replacement under heritage requirements", "Lightning protection system"]},
        "certs": ["VOB/B", "GEG"],
    },
    {
        "slug": "buergeramt-leonberg", "featured": False, "sample": True,
        "type": "administration", "city": "Leonberg", "size": "compact", "start": 2024, "end": 2024, "floors": 2, "seed": 29,
        "title": {"de": "Bürgeramt Leonberg", "en": "Leonberg citizens' office"},
        "client": {"de": "Stadt Leonberg, Amt für Gebäudemanagement", "en": "City of Leonberg, Building Management Office"},
        "budget": {"de": "ca. 0,6 Mio. € netto", "en": "approx. €0.6 m net"},
        "duration": {"de": "4 Monate", "en": "4 months"},
        "team": {"de": "Bauleiter, bis zu 10 Fachkräfte", "en": "Site manager, up to 10 specialists"},
        "summary": {"de": "Umbau des Publikumsbereichs mit barrierefreien Schaltern.", "en": "Conversion of the public area with accessible counters."},
        "scope": {"de": ["Neuer Wartebereich mit Aufrufsystem", "Barrierefreie Schalter und Leitsystem", "Akustikdecken"], "en": ["New waiting area with call system", "Accessible counters and guidance system", "Acoustic ceilings"]},
        "certs": ["VOB/B", "DIN 18040"],
    },
    {
        "slug": "sozialzentrum-stuttgart-ost", "featured": False, "sample": True,
        "type": "administration", "city": "Stuttgart", "size": "medium", "start": 2025, "end": 2025, "floors": 3, "seed": 31,
        "title": {"de": "Sozialzentrum Stuttgart-Ost", "en": "Stuttgart-Ost social centre"},
        "client": {"de": "Landeshauptstadt Stuttgart, Sozialamt", "en": "City of Stuttgart, Social Welfare Office"},
        "budget": {"de": "ca. 1,8 Mio. € netto", "en": "approx. €1.8 m net"},
        "duration": {"de": "9 Monate", "en": "9 months"},
        "team": {"de": "Bauleiterin, Polier, bis zu 20 Fachkräfte", "en": "Site manager, foreman, up to 20 specialists"},
        "summary": {"de": "Sanierung von Beratungs- und Büroflächen.", "en": "Refurbishment of counselling and office space."},
        "scope": {"de": ["Neuordnung der Grundrisse", "Brandschutzertüchtigung", "Erneuerung der Heizungsanlage"], "en": ["Reorganised floor plans", "Fire protection upgrade", "New heating system"]},
        "certs": ["VOB/B", "GEG", "ISO 9001"],
    },
    {
        "slug": "stadtbibliothek-filderstadt", "featured": False, "sample": True,
        "type": "culture", "city": "Filderstadt", "size": "medium", "start": 2021, "end": 2021, "floors": 2, "seed": 37,
        "title": {"de": "Stadtbibliothek Filderstadt", "en": "Filderstadt city library"},
        "client": {"de": "Stadt Filderstadt, Hochbauamt", "en": "City of Filderstadt, Building Construction Office"},
        "budget": {"de": "ca. 1,4 Mio. € netto", "en": "approx. €1.4 m net"},
        "duration": {"de": "8 Monate", "en": "8 months"},
        "team": {"de": "Bauleiter, Polier, bis zu 18 Fachkräfte", "en": "Site manager, foreman, up to 18 specialists"},
        "summary": {"de": "Modernisierung mit neuem Lesesaal und Klimatisierung.", "en": "Modernisation with a new reading room and air conditioning."},
        "scope": {"de": ["Umbau zum offenen Lesesaal", "Raumlufttechnik für Medienbestände", "Barrierefreie Erschließung"], "en": ["Conversion to an open reading room", "Ventilation and climate control for collections", "Step-free access"]},
        "certs": ["VOB/B", "GEG"],
    },
    {
        "slug": "stadtmuseum-ludwigsburg", "featured": False, "sample": True,
        "type": "culture", "city": "Ludwigsburg", "size": "large", "start": 2020, "end": 2021, "floors": 3, "seed": 41,
        "title": {"de": "Stadtmuseum Ludwigsburg", "en": "Ludwigsburg city museum"},
        "client": {"de": "Stadt Ludwigsburg, Fachbereich Hochbau und Gebäudewirtschaft", "en": "City of Ludwigsburg, Building Construction and Facility Department"},
        "budget": {"de": "ca. 2,7 Mio. € netto", "en": "approx. €2.7 m net"},
        "duration": {"de": "15 Monate", "en": "15 months"},
        "team": {"de": "Bauleiter, 2 Poliere, bis zu 26 Fachkräfte", "en": "Site manager, 2 foremen, up to 26 specialists"},
        "summary": {"de": "Sanierung eines denkmalgeschützten Gebäudes für den Museumsbetrieb.", "en": "Refurbishment of a listed building for museum use."},
        "scope": {"de": ["Statische Ertüchtigung der Geschossdecken", "Klimatechnik für Ausstellungsräume", "Abstimmung mit der Denkmalpflege"], "en": ["Structural strengthening of floor slabs", "Climate control for exhibition rooms", "Coordination with the heritage authority"]},
        "certs": ["VOB/B", "DIN", "ISO 9001"],
    },
    {
        "slug": "kulturzentrum-nuertingen", "featured": False, "sample": True,
        "type": "culture", "city": "Nürtingen", "size": "compact", "start": 2023, "end": 2023, "floors": 2, "seed": 43,
        "title": {"de": "Kulturzentrum Nürtingen", "en": "Nürtingen cultural centre"},
        "client": {"de": "Stadt Nürtingen, Amt für Gebäudewirtschaft", "en": "City of Nürtingen, Facility Management Office"},
        "budget": {"de": "ca. 0,9 Mio. € netto", "en": "approx. €0.9 m net"},
        "duration": {"de": "5 Monate", "en": "5 months"},
        "team": {"de": "Bauleiter, bis zu 12 Fachkräfte", "en": "Site manager, up to 12 specialists"},
        "summary": {"de": "Sanierung des Veranstaltungssaals.", "en": "Refurbishment of the event hall."},
        "scope": {"de": ["Raumakustik und Bühnentechnik-Vorbereitung", "Brandschutz für Versammlungsstätte", "Neue Lüftungsanlage"], "en": ["Room acoustics and preparation for stage technology", "Fire protection for a place of assembly", "New ventilation system"]},
        "certs": ["VOB/B", "DIN"],
    },
    {
        "slug": "pumpwerk-esslingen", "featured": False, "sample": True,
        "type": "infrastructure", "city": "Esslingen am Neckar", "size": "medium", "start": 2022, "end": 2022, "floors": 1, "seed": 47,
        "title": {"de": "Pumpwerk Esslingen-Mettingen", "en": "Esslingen-Mettingen pumping station"},
        "client": {"de": "Kommunaler Versorgungsbetrieb, Esslingen am Neckar", "en": "Municipal utility, Esslingen am Neckar"},
        "budget": {"de": "ca. 1,1 Mio. € netto", "en": "approx. €1.1 m net"},
        "duration": {"de": "6 Monate", "en": "6 months"},
        "team": {"de": "Bauleiter, Polier, bis zu 14 Fachkräfte", "en": "Site manager, foreman, up to 14 specialists"},
        "summary": {"de": "Bauliche Sanierung eines Pumpwerks bei laufender Versorgung.", "en": "Structural refurbishment of a pumping station while supply continued."},
        "scope": {"de": ["Betonsanierung und Abdichtung", "Neue Dachkonstruktion", "Vorbereitung für Maschinentechnik"], "en": ["Concrete repair and waterproofing", "New roof structure", "Preparation for mechanical equipment"]},
        "certs": ["VOB/B", "DIN"],
    },
    {
        "slug": "bauhof-ditzingen", "featured": False, "sample": True,
        "type": "infrastructure", "city": "Ditzingen", "size": "compact", "start": 2024, "end": 2025, "floors": 1, "seed": 53,
        "title": {"de": "Städtischer Bauhof Ditzingen", "en": "Ditzingen municipal depot"},
        "client": {"de": "Stadt Ditzingen, Tiefbau und Bauhof", "en": "City of Ditzingen, Civil Engineering and Depot"},
        "budget": {"de": "ca. 0,7 Mio. € netto", "en": "approx. €0.7 m net"},
        "duration": {"de": "7 Monate", "en": "7 months"},
        "team": {"de": "Bauleiter, bis zu 10 Fachkräfte", "en": "Site manager, up to 10 specialists"},
        "summary": {"de": "Neubau einer Fahrzeughalle mit Werkstatt.", "en": "New vehicle hall with workshop."},
        "scope": {"de": ["Hallenneubau in Stahlbauweise", "Werkstatt und Sozialräume", "Photovoltaikanlage"], "en": ["New steel-frame hall", "Workshop and staff rooms", "Photovoltaic system"]},
        "certs": ["VOB/B", "GEG"],
    },
]
