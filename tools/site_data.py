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
    "street": "Eichendorffstraße 3",
    "zip_city": "40474 Düsseldorf",
    "country": {"de": "Deutschland", "en": "Germany"},
    "email": "info@sdtt.de",
    "phone": ("+49 176 74906009", "+4917674906009"),
    "emergency": ("+49 1515 8826480", "+4915158826480"),
    "whatsapp": ("+49 1573 5144487", "4915735144487"),
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
        "name": "Denys Danilovskyi",
        "photo": "assets/img/team/denys-danilovskyi.jpg",
        "email": "ausschreibung@sdtrockenbau.com",
        "phone": ("+49 1573 5144487", "+4915735144487"),
        "office": "Wilhelmstraße 45, 70182 Stuttgart",
        "focus": {"de": "Vergabeverfahren, Angebote und Eignungsnachweise", "en": "Tender procedures, bids and proof of eligibility"},
        "fn": {
            "de": "Koordiniert alle öffentlichen Ausschreibungen, Angebote und Eignungsnachweise sowie die Abstimmung mit Vergabestellen und Behörden.",
            "en": "Coordinates all public tenders, bids and proof-of-eligibility documents, and liaises with contracting authorities.",
        },
    },
    {
        "key": "technical",
        "role": {"de": "Technische Leitung", "en": "Technical department"},
        "role_de": "Technischer Leiter",
        "name": "Maksym Yuzenko",
        "photo": "assets/img/team/maksym-yuzenko.jpg",
        "email": "my@sdtrockenbau.com",
        "phone": ("+49 176 74906009", "+4917674906009"),
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
        "name": "Kateryna Seledkova",
        "photo": "assets/img/team/kateryna-seledkova.jpg",
        "email": "qualität@sdtrockenbau.com",
        "phone": ("+49 155 67663864", "+4915567663864"),
        "office": None,
        "focus": {"de": "Qualitätssicherung, externe Audits und Abnahmen", "en": "Quality assurance, external audits and acceptance"},
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
        "slug": "schulsanierung-stuttgart",
        "featured": True, "sample": False,
        "photos": {"ext": "jpg", "w": 1200, "h": 1607},
        "type": "education", "city": "Stuttgart", "size": "medium", "start": 2023, "end": 2024,
        "floors": 4, "seed": 3,
        "title": {"de": "Gemeinschaftsschule Stuttgart", "en": "Community school, Stuttgart"},
        "client": {"de": "Landeshauptstadt Stuttgart, Schulverwaltungsamt", "en": "City of Stuttgart, School Administration Office"},
        "budget": {"de": "ca. 1 Mio. € netto", "en": "approx. €1 m net"},
        "duration": {"de": "6 Monate, zwei Bauabschnitte", "en": "6 months, two construction phases"},
        "team": {"de": "Bauleiter, 2 Poliere, bis zu 24 eigene Fachkräfte", "en": "Site manager, 2 foremen, up to 24 in-house specialists"},
        "summary": {
            "de": "Sanierung der Flure einer weiterführenden Schule im laufenden Unterrichtsbetrieb.",
            "en": "Refurbishment of the corridors of a secondary school while classes continued.",
        },
        "scope": {
            "de": ["Austausch des Bodenbelags", "Malerarbeiten an den Wänden", "Trockenbau: Gipskartonkonstruktionen und Umbauten", "Austausch der Fenster"],
            "en": ["Replacement of the flooring", "Painting of the walls", "Drywall construction: plasterboard structures and alterations", "Replacement of the windows"],
        },
        "text": {
            "de": [
                "Die Flure der weiterführenden Schule wurden in zwei Bauabschnitten saniert, sodass der Unterricht ohne Unterbrechung weiterlaufen konnte. Lärmintensive Arbeiten wurden mit der Schulleitung in die Ferienzeiten und auf die Nachmittage gelegt.",
                "Bodenbelag, Wandanstriche, Trockenbauflächen und Fenster wurden in einem Zug erneuert. Der Auftraggeber erhielt wöchentliche Baufortschritts- und Kostenberichte sowie eine vollständige Bestandsdokumentation zur Abnahme.",
            ],
            "en": [
                "The corridors of the secondary school were refurbished in two construction phases so that teaching could continue without interruption. Noisy work was scheduled with the school management during holidays and in the afternoons.",
                "Flooring, wall paint, drywall surfaces and windows were renewed in one go. The client received weekly progress and cost reports and complete as-built documentation at acceptance.",
            ],
        },
        "certs": ["VOB/B", "DIN", "GEG", "ISO 9001"],
        "contact": {"name": "Herr Klaus Müller", "email": "k.mueller@stuttgart.example", "phone": ("+49 711 0000-2000", "+4971100002000")},
    },
    {
        "slug": "sozialzentrum-ludwigsburg",
        "featured": True, "sample": False,
        "photos": {"ext": "jpg", "w": 1200, "h": 1608},
        "type": "administration", "city": "Ludwigsburg", "size": "compact", "start": 2022, "end": 2023,
        "floors": 3, "seed": 5,
        "title": {"de": "Sozialzentrum Ludwigsburg", "en": "Ludwigsburg social centre"},
        "client": {"de": "Stadt Ludwigsburg, Fachbereich Bürgerschaftliches Engagement und Soziales", "en": "City of Ludwigsburg, Department of Civic Engagement and Social Affairs"},
        "budget": {"de": "ca. 0,9 Mio. € netto", "en": "approx. €0.9 m net"},
        "duration": {"de": "7 Monate", "en": "7 months"},
        "team": {"de": "Bauleiterin, Polier, bis zu 19 eigene Fachkräfte", "en": "Site manager, foreman, up to 19 in-house specialists"},
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
                "Das Sozialzentrum wurde während der Bauzeit teilweise weiter genutzt. Beratungsangebote zogen abschnittsweise in bereits fertiggestellte Bereiche um.",
                "Schwerpunkte waren Barrierefreiheit und Brandschutz. Alle Nachträge wurden vor Ausführung schriftlich vom Auftraggeber freigegeben.",
            ],
            "en": [
                "The social centre remained partly in use during construction. Counselling services moved section by section into areas that were already finished.",
                "The focus was on accessibility and fire protection. All change orders were approved in writing by the client before execution.",
            ],
        },
        "certs": ["VOB/B", "DIN 18040", "GEG", "ISO 9001"],
        "contact": {"name": "Frau Andrea Weber", "email": "a.weber@ludwigsburg.example", "phone": ("+49 7141 0000-300", "+49714100003000")},
    },
    {
        "slug": "rathaus-gerlingen",
        "featured": True, "sample": False,
        "photos": {"ext": "jpg", "w": 1200, "h": 1608},
        "type": "administration", "city": "Gerlingen", "size": "medium", "start": 2025, "end": 2026,
        "floors": 2, "seed": 7,
        "title": {"de": "Rathaus Gerlingen", "en": "Gerlingen town hall"},
        "client": {"de": "Stadt Gerlingen, Hochbauamt", "en": "City of Gerlingen, Building Construction Office"},
        "budget": {"de": "ca. 1,8 Mio. € netto", "en": "approx. €1.8 m net"},
        "duration": {"de": "10 Monate, abschnittsweise je Geschoss", "en": "10 months, floor by floor"},
        "team": {"de": "Bauleiter, 3 Poliere, bis zu 30 eigene Fachkräfte", "en": "Site manager, 3 foremen, up to 30 in-house specialists"},
        "summary": {
            "de": "Modernisierung der Verwaltungsflure im Rathaus einer Kleinstadt bei laufendem Betrieb.",
            "en": "Modernisation of the administrative corridors in a small-town town hall while it remained in operation.",
        },
        "scope": {
            "de": ["Austausch der Türen", "Austausch der Fenster", "Trockenbauarbeiten", "Neue Bodenbeläge", "Neue Deckenverkleidungen", "Neue Beleuchtung und Gebäudetechnik"],
            "en": ["Replacement of the doors", "Replacement of the windows", "Drywall construction", "New flooring", "New ceiling linings", "New lighting and building services"],
        },
        "text": {
            "de": [
                "Das Rathaus blieb während der Bauzeit geöffnet. Die Arbeiten erfolgten abschnittsweise je Geschoss, Bürgerservice und Verwaltung zogen stufenweise in bereits fertiggestellte Bereiche um.",
                "Türen, Fenster, Trockenbau, Bodenbeläge, Decken, Beleuchtung und Gebäudetechnik wurden aufeinander abgestimmt ausgeführt. Die Fertigstellung erfolgte 2026 termingerecht und im Rahmen des Budgets.",
            ],
            "en": [
                "The town hall stayed open throughout construction. The work was carried out floor by floor, and citizen services and administration moved step by step into areas that were already finished.",
                "Doors, windows, drywall, flooring, ceilings, lighting and building services were carried out in a coordinated sequence. The project was completed in 2026 on schedule and within budget.",
            ],
        },
        "certs": ["VOB/B", "DIN", "GEG", "ISO 9001"],
        "contact": {"name": "Herr Markus Bauer", "email": "m.bauer@gerlingen.example", "phone": ("+49 7156 0000-200", "+49715600000200")},
    },
    # ---- Sample projects (Musterdaten) ----
    {
        "slug": "kreisklinik-boeblingen", "featured": False, "sample": False,
        "photos": {"ext": "jpg", "w": 1200, "h": 1608},
        "type": "health", "city": "Böblingen", "size": "compact", "start": 2023, "end": 2024, "floors": 1, "seed": 17,
        "title": {"de": "Kreisklinik Böblingen, Umbau Eingangsbereich", "en": "District hospital Böblingen, entrance area conversion"},
        "client": {"de": "Kommunaler Klinikträger, Landkreis Böblingen", "en": "Municipal hospital operator, Böblingen district"},
        "budget": {"de": "ca. 0,7 Mio. € netto", "en": "approx. €0.7 m net"},
        "duration": {"de": "5 Monate im laufenden Klinikbetrieb", "en": "5 months while the hospital remained in operation"},
        "team": {"de": "Bauleiter, Polier, bis zu 12 eigene Fachkräfte", "en": "Site manager, foreman, up to 12 in-house specialists"},
        "summary": {
            "de": "Umbau und Modernisierung des Eingangsbereichs einer Kreisklinik im laufenden Betrieb.",
            "en": "Conversion and modernisation of the entrance area of a district hospital while it remained in operation.",
        },
        "scope": {
            "de": ["Staubschutz- und Hygienekonzept für den laufenden Betrieb", "Austausch der Fenster und der Eingangsfassade", "Wärmedämmung der Fassade im Eingangsbereich", "Trockenbau: Wände, Empfangstheke und Akustikdecken", "Neue Bodenbeläge", "Neue Beleuchtung"],
            "en": ["Dust protection and hygiene concept for continued operation", "Replacement of the windows and the entrance facade", "Thermal insulation of the facade in the entrance area", "Drywall construction: walls, reception counter and acoustic ceilings", "New flooring", "New lighting"],
        },
        "text": {
            "de": [
                "Der Eingangs- und Empfangsbereich der Kreisklinik wurde bei laufendem Klinikbetrieb umgebaut. Staubschutzwände und ein abgestimmtes Hygienekonzept sorgten dafür, dass Patientenwege und Notaufnahme jederzeit frei blieben.",
                "Fenster und Eingangsfassade, Fassadendämmung, Trockenbau, Akustikdecken, Bodenbeläge und Beleuchtung wurden in zwei Bauabschnitten ausgeführt. Der Auftraggeber erhielt wöchentliche Baufortschritts- und Kostenberichte.",
            ],
            "en": [
                "The entrance and reception area of the district hospital was converted while the hospital stayed in operation. Dust-protection walls and a coordinated hygiene concept kept patient routes and the emergency entrance open at all times.",
                "Windows and entrance facade, facade insulation, drywall, acoustic ceilings, flooring and lighting were carried out in two construction phases. The client received weekly progress and cost reports.",
            ],
        },
        "certs": ["VOB/B", "DIN", "GEG", "ISO 9001"],
    },
    {
        "slug": "stadtbibliothek-filderstadt", "featured": False, "sample": False,
        "photos": {"ext": "jpg", "w": 1200, "h": 1608},
        "type": "culture", "city": "Filderstadt", "size": "medium", "start": 2023, "end": 2024, "floors": 2, "seed": 37,
        "title": {"de": "Stadtbibliothek Filderstadt", "en": "Filderstadt city library"},
        "client": {"de": "Stadt Filderstadt, Hochbauamt", "en": "City of Filderstadt, Building Construction Office"},
        "budget": {"de": "ca. 1,4 Mio. € netto", "en": "approx. €1.4 m net"},
        "duration": {"de": "8 Monate, zwei Bauabschnitte", "en": "8 months, two construction phases"},
        "team": {"de": "Bauleiter, 2 Poliere, bis zu 18 eigene Fachkräfte", "en": "Site manager, 2 foremen, up to 18 in-house specialists"},
        "summary": {
            "de": "Modernisierung einer Stadtbibliothek mit offenem Lesesaal, Arbeitsnischen und neuer Klimatisierung.",
            "en": "Modernisation of a city library with an open reading room, study alcoves and new climate control.",
        },
        "scope": {
            "de": ["Trockenbau: neue Wände, Arbeitsnischen und Deckenfelder", "Offene Metalldecken mit Raumlufttechnik", "Neue Bodenbeläge: Estrich und Teppichfliesen", "Neue Beleuchtung mit Stromschienen", "Barrierefreie Erschließung", "Malerarbeiten"],
            "en": ["Drywall construction: new walls, study alcoves and ceiling panels", "Open metal ceilings with ventilation", "New flooring: screed and carpet tiles", "New lighting on track systems", "Step-free access", "Painting works"],
        },
        "text": {
            "de": [
                "Die Stadtbibliothek wurde in zwei Bauabschnitten modernisiert, sodass ein Teil der Medienbestände und Leseplätze während der Bauzeit nutzbar blieb. Staub- und Lärmschutz wurden mit der Bibliotheksleitung abgestimmt.",
                "Trockenbau, Deckensysteme, Raumlufttechnik, Bodenbeläge und Beleuchtung wurden aufeinander abgestimmt ausgeführt. Der Auftraggeber erhielt wöchentliche Baufortschritts- und Kostenberichte sowie eine vollständige Bestandsdokumentation zur Abnahme.",
            ],
            "en": [
                "The city library was modernised in two construction phases so that part of the collection and reading places remained usable during construction. Dust and noise protection were agreed with the library management.",
                "Drywall, ceiling systems, ventilation, flooring and lighting were carried out in a coordinated sequence. The client received weekly progress and cost reports and complete as-built documentation at acceptance.",
            ],
        },
        "certs": ["VOB/B", "DIN", "GEG", "ISO 9001"],
    },
]
