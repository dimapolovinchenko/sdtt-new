"""Download documents (PDF) for the SDTT site: project archive, standards, references,
key personnel, methodology, warranty, insurance and guarantees. German and English.

Only information that is already on the website is used. Nothing here is a certificate, a signed
reference letter or an insurance policy: where such originals exist they are available on request.
Run through build.py (build_pdfs)."""
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

NAVY = colors.HexColor("#1A3D66")
GREY = colors.HexColor("#F0F0F2")
LINE = colors.HexColor("#D5D8DE")
TEXT = colors.HexColor("#2A2A2A")
MUTED = colors.HexColor("#555B66")
GREEN = colors.HexColor("#4A7C59")

W, H = A4
M = 20 * mm

S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=NAVY, spaceAfter=4),
    "lead": ParagraphStyle("lead", fontName="Helvetica", fontSize=12, leading=17, textColor=MUTED, spaceAfter=14),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=NAVY, spaceBefore=14, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=TEXT, spaceBefore=8, spaceAfter=2),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=10.5, leading=15, textColor=TEXT, spaceAfter=6, alignment=TA_LEFT),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9, leading=12.5, textColor=MUTED),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9.5, leading=13, textColor=TEXT),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=TEXT),
    "th": ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.white),
    "li": ParagraphStyle("li", fontName="Helvetica", fontSize=10.5, leading=15, textColor=TEXT, leftIndent=12, bulletIndent=0, spaceAfter=2),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def P(text, style="p"):
    return Paragraph(esc(text), S[style])


def bullets(items):
    return [Paragraph(esc(i), S["li"], bulletText="•") for i in items]


def logo(c, x, y, size):
    """The SDTT mark (four squares, one with an inner frame) drawn as vector shapes."""
    u = size / 124.0
    c.setFillColor(NAVY)
    for (qx, qy) in [(0, 68), (68, 68), (0, 0)]:
        c.rect(x + qx * u, y + qy * u, 56 * u, 56 * u, stroke=0, fill=1)
    c.rect(x + 68 * u, y, 56 * u, 56 * u, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.rect(x + 76 * u, y + 8 * u, 40 * u, 40 * u, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(x + 84 * u, y + 16 * u, 24 * u, 24 * u, stroke=0, fill=1)


def make(story, lang, co, doc_title):
    de = lang == "de"
    buf = io.BytesIO()
    foot = f"SDTT GmbH · {co['street']} · {co['zip_city']} · {co['email']}"
    stand = "Stand: Oktober 2026" if de else "As of October 2026"

    def page(c, d):
        c.saveState()
        logo(c, M, H - 22 * mm, 11 * mm)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 17)
        c.drawString(M + 15 * mm, H - 16.5 * mm, "S D T T")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(MUTED)
        c.drawString(M + 15 * mm, H - 20.5 * mm, "G E N E R A L U N T E R N E H M E R" if de else "G E N E R A L   C O N T R A C T O R")
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(M, H - 26 * mm, W - M, H - 26 * mm)
        c.line(M, 17 * mm, W - M, 17 * mm)
        c.setFont("Helvetica", 8)
        c.setFillColor(MUTED)
        c.drawString(M, 12 * mm, foot)
        c.drawRightString(W - M, 12 * mm, f"{stand} · {'Seite' if de else 'Page'} {d.page}")
        c.restoreState()

    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=34 * mm, bottomMargin=24 * mm,
                          title=doc_title, author="SDTT GmbH")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(M, 24 * mm, W - 2 * M, H - 58 * mm, id="f", leftPadding=0,
                                                              rightPadding=0, topPadding=0, bottomPadding=0)], onPage=page)])
    doc.build(story)
    return buf.getvalue()


def table(rows, widths, header=True):
    data = []
    for ri, r in enumerate(rows):
        data.append([c if not isinstance(c, str) else Paragraph(esc(c), S["th" if (header and ri == 0) else "cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
          ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
          ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    t.setStyle(TableStyle(st))
    return t


def head(title, lead):
    return [P(title, "title"), P(lead, "lead")]


# ---------------------------------------------------------------- documents
def archive(lang, D, period):
    de = lang == "de"
    out = head("Projektarchiv" if de else "Project archive",
               "Referenzprojekte für öffentliche Auftraggeber in Baden-Württemberg." if de else
               "Reference projects for public clients in Baden-Württemberg.")
    rows = [["Projekt" if de else "Project", "Zeitraum" if de else "Period", "Volumen" if de else "Value"]]
    for p in D.PROJECTS:
        rows.append([f"{p['title'][lang]}\n{p['city']}".replace("\n", "<br/>") if False else p["title"][lang] + " – " + p["city"],
                     period(p), p["budget"][lang].replace(" netto", "").replace(" net", "")])
    out.append(table(rows, [95 * mm, 30 * mm, 45 * mm]))
    for p in D.PROJECTS:
        out.append(KeepTogether([
            P(p["title"][lang], "h2"),
            P(p["summary"][lang]),
            table([
                ["Zeitraum" if de else "Period", f"{period(p)} · {p['duration'][lang]}"],
                ["Auftraggeber" if de else "Client", p["client"][lang]],
                ["Auftragsvolumen" if de else "Contract value", p["budget"][lang]],
                ["Team", p["team"][lang]],
            ], [40 * mm, 130 * mm], header=False),
            P("Leistungsumfang" if de else "Scope of works", "h3"),
            *bullets(p["scope"][lang]),
        ]))
    return out


def standards(lang, D, period):
    de = lang == "de"
    out = head("Normen und Zertifikate" if de else "Standards and certificates",
               "Die Grundlagen unserer Arbeit für öffentliche Auftraggeber." if de else
               "The foundations of our work for public clients.")
    items = [
        ("ISO 9001:2015 – " + ("Qualitätsmanagement" if de else "Quality management"),
         "Dokumentierte Prozesse von der Kalkulation bis zur Abnahme, regelmäßige interne Audits, Rückverfolgbarkeit von Materialien und Prüfungen."
         if de else "Documented processes from estimating to acceptance, regular internal audits, traceability of materials and inspections."),
        ("VOB/B · VOB/C · DIN",
         "Ausführung aller Leistungen nach VOB/B und VOB/C sowie den einschlägigen DIN-Normen; transparente Abrechnung nach Aufmaß; förmliche Abnahme nach § 12 VOB/B."
         if de else "All works are carried out to VOB/B, VOB/C and the relevant DIN standards; transparent invoicing by measured quantities; formal acceptance under § 12 VOB/B."),
        ("GEG – " + ("Gebäudeenergiegesetz" if de else "Buildings Energy Act"),
         "Energetische Sanierungen und Neubauten nach den Anforderungen des GEG, mit dokumentierten Nachweisen für den Auftraggeber."
         if de else "Energy refurbishments and new buildings to the requirements of the GEG, with documented proof for the client."),
        ("DGUV Regel 100-001 – " + ("Arbeitsschutz" if de else "Occupational safety"),
         "Jährliche, dokumentierte Unterweisung aller Beschäftigten und Arbeitsschutz auf jeder Baustelle."
         if de else "Annual documented safety training for all employees and occupational safety on every site."),
        ("§ 634a BGB – " + ("Gewährleistung" if de else "Warranty"),
         "Fünf Jahre Mängelhaftung bei Bauwerken, Mängelbeseitigung durch eigenes Personal."
         if de else "Five years' liability for defects in buildings, remedied by our own staff."),
    ]
    for t, x in items:
        out.append(KeepTogether([P(t, "h2"), P(x)]))
    out.append(P("Nachweise" if de else "Proof", "h2"))
    out.append(P("Zertifikate, Prüfberichte und Konformitätsnachweise stellen wir Vergabestellen auf Anfrage und projektbezogen zur Verfügung."
                 if de else "We provide certificates, test reports and proof of conformity to contracting authorities on request and per project."))
    return out


def references(lang, D, period):
    de = lang == "de"
    out = head("Referenzen" if de else "References",
               "Auftraggeber und Eckdaten unserer Referenzprojekte." if de else "Clients and key data of our reference projects.")
    t = [[Paragraph(esc("Projekt" if de else "Project"), S["th"]), Paragraph(esc("Auftraggeber" if de else "Client"), S["th"]),
          Paragraph(esc("Zeitraum · Volumen" if de else "Period · value"), S["th"])]]
    for p in D.PROJECTS:
        t.append([Paragraph(esc(p["title"][lang]), S["cellb"]), Paragraph(esc(p["client"][lang]), S["cell"]),
                  Paragraph(esc(period(p)) + "<br/>" + esc(p["budget"][lang]), S["cell"])])
    tb = Table(t, colWidths=[58 * mm, 72 * mm, 40 * mm], repeatRows=1)
    tb.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                            ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    out.append(tb)
    out.append(Spacer(1, 10))
    out.append(P("Referenzschreiben der Auftraggeber sowie Ansprechpartner bei den Auftraggebern nennen wir – mit deren Einverständnis – auf Anfrage."
                 if de else "We provide reference letters from clients and client contacts, with their consent, on request."))
    return out


def personnel(lang, D, period):
    de = lang == "de"
    out = head("Schlüsselpersonal" if de else "Key personnel",
               "Feste Ansprechpartner für Vergabestellen – von der Angebotsphase bis zur Abnahme." if de else
               "Dedicated contacts for contracting authorities – from the bidding phase to acceptance.")
    people = [D.DIRECTOR] + D.PEOPLE
    for p in people:
        block = [P(p["name"], "h2"), P(p["role"][lang], "h3")]
        if p.get("fn"):
            block.append(P(p["fn"][lang]))
        if p.get("focus"):
            block.append(P(("Schwerpunkt: " if de else "Focus: ") + p["focus"][lang]))
        block.append(P(f"{'E-Mail' if de else 'Email'}: {p['email']}   ·   {'Telefon' if de else 'Phone'}: {p['phone'][0]}", "small"))
        out.append(KeepTogether(block))
    out.append(Spacer(1, 12))
    out.append(P("Qualifikationsnachweise und Lebensläufe des eingesetzten Fach- und Leitungspersonals reichen wir projektbezogen mit dem Angebot ein."
                 if de else "We submit qualification proof and CVs of the site management and specialists deployed on a project together with the bid."))
    return out


def methodology(lang, D, period):
    de = lang == "de"
    out = head("Projektmanagement-Methodik" if de else "Project management methodology",
               "Ein festgelegter Ablauf mit klaren Berichtspflichten – vom Projektstart bis zur Gewährleistung." if de else
               "A defined process with clear reporting duties – from project start to the warranty period.")
    steps = [
        ("Projektstart und Bauablaufplanung" if de else "Project start and scheduling",
         "Abstimmung mit Auftraggeber und Fachplanern, Terminplan mit Pufferzeiten, Baustelleneinrichtung." if de else
         "Coordination with the client and specialist designers, schedule with buffers, site set-up."),
        ("Kostenaufstellung" if de else "Cost breakdown",
         "Detaillierte Kostenaufstellung 30 Tage vor Baubeginn, Freigabe durch den Auftraggeber." if de else
         "Detailed cost breakdown 30 days before construction starts, approved by the client."),
        ("Ausführung mit Wochenberichten" if de else "Execution with weekly reports",
         "Baufortschritts- und Soll-Ist-Kostenberichte jede Woche, Nachträge nur nach schriftlicher Beauftragung." if de else
         "Progress and budget-versus-actual reports every week, change orders only after written instruction."),
        ("Qualitätssicherung" if de else "Quality assurance",
         "Eigene Prüfungen nach ISO 9001 und Begleitung durch unabhängige Prüfer." if de else
         "In-house inspections to ISO 9001 and support from independent inspectors."),
        ("Abnahme und Dokumentation" if de else "Acceptance and documentation",
         "Förmliche Abnahme, Übergabe von Bestandsplänen, Materialnachweisen und Prüfprotokollen." if de else
         "Formal acceptance, handover of as-built drawings, material certificates and test reports."),
        ("Gewährleistung" if de else "Warranty",
         "Fünf Jahre Mängelhaftung, Mängelbeseitigung durch eigenes Personal." if de else
         "Five years' liability for defects, remedied by our own staff."),
    ]
    for i, (t, x) in enumerate(steps, 1):
        out.append(KeepTogether([P(f"{i:02d}  {t}", "h2"), P(x)]))
    return out


def warranty(lang, D, period):
    de = lang == "de"
    out = head("Gewährleistungsbedingungen" if de else "Warranty terms",
               "Mängelhaftung nach § 634a BGB." if de else "Liability for defects under § 634a BGB.")
    for t, x in [
        ("Verjährungsfrist" if de else "Limitation period",
         "Für Bauwerke gilt eine Verjährungsfrist für Mängelansprüche von fünf Jahren ab Abnahme (§ 634a BGB). Bei VOB/B-Verträgen vereinbaren wir auf Wunsch ebenfalls fünf Jahre anstelle der Regelfrist von vier Jahren (§ 13 Abs. 4 VOB/B)." if de else
         "For buildings, claims for defects become time-barred five years after acceptance (§ 634a BGB). For VOB/B contracts we also agree five years on request instead of the standard four years (§ 13(4) VOB/B)."),
        ("Mängelbeseitigung" if de else "Remedying defects",
         "Mängel werden durch unser eigenes Personal beseitigt. Gemeldete Mängel werden dokumentiert und in einem mit dem Auftraggeber abgestimmten Zeitraum behoben." if de else
         "Defects are remedied by our own staff. Reported defects are documented and rectified within a period agreed with the client."),
        ("Abnahme" if de else "Acceptance",
         "Die Gewährleistungsfrist beginnt mit der förmlichen Abnahme nach § 12 VOB/B. Bestandsunterlagen, Materialnachweise und Prüfprotokolle werden bei der Abnahme übergeben." if de else
         "The warranty period starts with formal acceptance under § 12 VOB/B. As-built documents, material certificates and test reports are handed over at acceptance."),
        ("Sicherheit" if de else "Security",
         "Auf Wunsch stellen wir eine Gewährleistungsbürgschaft nach § 17 VOB/B." if de else
         "On request we provide a warranty guarantee under § 17 VOB/B."),
    ]:
        out.append(KeepTogether([P(t, "h2"), P(x)]))
    return out


def insurance(lang, D, period):
    de = lang == "de"
    out = head("Versicherungsnachweis und Bürgschaften" if de else "Proof of insurance and guarantees",
               "Absicherung für öffentliche Auftraggeber." if de else "Protection for public clients.")
    for t, x in [
        ("Betriebshaftpflicht" if de else "Business liability insurance",
         "Absicherung von Personen-, Sach- und Vermögensschäden, die im Rahmen der Bauausführung entstehen können." if de else
         "Cover for personal injury, property damage and financial loss that may arise during construction."),
        ("Bauleistungsversicherung" if de else "Contractor's all-risk insurance",
         "Absicherung der Bauleistung gegen Beschädigung und Zerstörung bis zur Abnahme." if de else
         "Cover for the works against damage and destruction until acceptance."),
        ("Bürgschaften" if de else "Guarantees",
         "Vertragserfüllungs- und Gewährleistungsbürgschaften stellen wir nach § 17 VOB/B im Umfang der Vergabeunterlagen." if de else
         "We provide performance and warranty guarantees under § 17 VOB/B to the extent required in the tender documents."),
        ("Nachweise" if de else "Proof",
         "Aktuelle Versicherungsbestätigungen und Bürgschaftsurkunden reichen wir projektbezogen mit dem Angebot bzw. nach Zuschlag ein." if de else
         "We submit current insurance confirmations and guarantee documents per project, with the bid or after award."),
    ]:
        out.append(KeepTogether([P(t, "h2"), P(x)]))
    return out


BUILDERS = {
    "archive": archive, "certificates": standards, "references": references,
    "cvs": personnel, "methodology": methodology, "warranty": warranty, "insurance": insurance,
}


def build(doc, lang, D, period):
    return make(BUILDERS[doc["key"]](lang, D, period), lang, D.COMPANY, doc["title"][lang])
