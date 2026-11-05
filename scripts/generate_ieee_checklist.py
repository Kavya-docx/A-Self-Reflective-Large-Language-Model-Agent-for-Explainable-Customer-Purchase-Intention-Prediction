from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "ieee_2026_purchase_intention_checklist.pdf"
BLUE = colors.HexColor("#284C76")
LIGHT_BLUE = colors.HexColor("#E8EEF6")
LINE = colors.HexColor("#D8E0EA")
TEXT = colors.HexColor("#2F4053")


def item(text: str) -> str:
    return "[ ]  " + text


def checklist_table(rows, width=170 * mm):
    data = [[Paragraph(row, STYLES["Row"]) for row in rows]]
    return Table(data, colWidths=[width], style=TableStyle([("GRID", (0, 0), (-1, -1), .35, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))


STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name="TitleBlue", parent=STYLES["Title"], fontName="Helvetica-Bold", fontSize=19, leading=23, alignment=TA_CENTER, textColor=BLUE, spaceAfter=12))
STYLES.add(ParagraphStyle(name="Intro", parent=STYLES["Normal"], fontSize=8.5, leading=12, textColor=TEXT, spaceAfter=6))
STYLES.add(ParagraphStyle(name="SectionBlue", parent=STYLES["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=BLUE, spaceBefore=9, spaceAfter=5))
STYLES.add(ParagraphStyle(name="Row", parent=STYLES["Normal"], fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=TEXT))
STYLES.add(ParagraphStyle(name="Small", parent=STYLES["Normal"], fontSize=7.5, leading=10, textColor=colors.HexColor("#66798C")))


def build_checklist():
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=16 * mm, bottomMargin=18 * mm)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.line(18 * mm, 13 * mm, 192 * mm, 13 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#66798C"))
        canvas.drawString(18 * mm, 8 * mm, "IEEE 2026 Project Report and Submission Checklist")
        canvas.drawRightString(192 * mm, 8 * mm, f"Page {doc.page} of 2")
        canvas.restoreState()

    story = [
        Spacer(1, 4 * mm),
        Paragraph("IEEE 2026 | PROJECT REPORT & SUBMISSION CHECKLIST", STYLES["TitleBlue"]),
        Paragraph("Use one copy for the project: <b>Self-Reflective Large-Language-Model Agent for Explainable Customer Purchase Intention Prediction</b>.", STYLES["Intro"]),
        Paragraph("Project No.: ____________________   Owner: ______________________________   Sector: Retail / E-Commerce", STYLES["Intro"]),
        Paragraph("Project Title: __________________________________________________________________________________", STYLES["Intro"]),
        Paragraph("Review Date: ____________________   Reviewer: ___________________________   Version: 1.0", STYLES["Intro"]),
        Paragraph("A. REPORT CHAPTERS", STYLES["SectionBlue"]),
        checklist_table([item("Preliminary pages: cover page, abstract, keywords, contents, figures and tables"), item("1. Introduction: customer purchase-intention problem, objectives, motivation, scope and research questions"), item("2. Literature review: explainable AI, purchase prediction, self-reflection, human-in-the-loop systems"), item("3. Existing versus proposed system: limitations, novelty, contributions and design choices"), item("4. Architecture: end-to-end diagram, data flow, agent flow, API flow and deployment path"), item("5. Dataset: synthetic-data provenance, feature dictionary, target definition, validation and limitations"), item("6. Methodology: logistic regression, preprocessing, signed contributions, reflection checks and counterfactuals"), item("7. Implementation: FastAPI, SQLite audit store, browser UI, credentials, Vercel entrypoint and configuration"), item("8. Experimental setup: seed, sample count, train-test split, baselines, metrics and reproducibility commands"), item("9. Results and discussion: ROC-AUC, accuracy, Brier score, examples, confidence and error analysis"), item("10. Conclusion and future work: production data, calibration, drift, durable storage and local LLM extension")]),
        Paragraph("B. PROJECT-SPECIFIC AI CHECKLIST", STYLES["SectionBlue"]),
        checklist_table([item("Three outputs are clearly defined: intention, decision evidence, and self-reflection"), item("The model output includes probability, risk band, positive factors, negative factors and confidence"), item("The reflection layer checks input quality, confidence, explanation availability and boundary stability"), item("Counterfactual suggestions are labelled as guidance, not causal proof"), item("Human review is recommended for low-confidence or invalid cases"), item("No unsupported claim is made that synthetic-data metrics represent production performance")]),
        Paragraph("C. FIGURES AND TABLES", STYLES["SectionBlue"]),
        checklist_table([item("System architecture diagram included and explained in the text"), item("Prediction sequence or data-flow diagram included"), item("Feature dictionary and validation rules included"), item("Model evaluation table includes ROC-AUC 0.7949, accuracy 0.7375, Brier score 0.1801 and 160 test samples"), item("Screenshots include the credential login, assessment form and three-output result view")]),
        PageBreak(),
        Paragraph("D. DATA, ETHICS AND PRIVACY", STYLES["SectionBlue"]),
        checklist_table([item("Target is explicitly defined as purchase within the selected observation window"), item("Synthetic data is clearly labelled and not presented as real customer evidence"), item("No names, emails, addresses or direct personal identifiers are required by the schema"), item("Consent, retention, deletion and access-control plans are documented for future real data"), item("Fairness and subgroup evaluation are listed as required production work"), item("Limitations of behavioural proxies and counterfactual interpretation are disclosed")]),
        Paragraph("E. SECURITY AND DEPLOYMENT", STYLES["SectionBlue"]),
        checklist_table([item("APP_USERNAME, APP_PASSWORD and SESSION_SECRET are configured as Vercel environment variables"), item("No password, token or session secret appears in Git history"), item("Login creates an HTTP-only, signed, eight-hour session cookie"), item("/predict and /model/metrics reject unauthenticated requests with HTTP 401"), item("Secure cookie behaviour is verified on the HTTPS production URL"), item("Ephemeral Vercel /tmp storage is documented and not treated as durable audit storage"), item("Production database, rate limiting, secret rotation, monitoring and incident response are planned")]),
        Paragraph("F. REPRODUCIBILITY AND TESTING", STYLES["SectionBlue"]),
        checklist_table([item("README includes local setup, training and deployment instructions"), item("pyproject.toml and requirements.txt specify open-source dependencies"), item("Random seed and sample count are recorded for the verified run"), item("pytest completes successfully with 3 passing tests"), item("Unauthorized, login and authenticated prediction smoke checks are recorded"), item("The three-output API contract is tested in the regression suite"), item("A reproducible report and IEEE paper generator are included")]),
        Paragraph("G. SUBMISSION PACKAGE", STYLES["SectionBlue"]),
        checklist_table([item("Source repository URL: https://github.com/Kavya-docx/A-Self-Reflective-Large-Language-Model-Agent-for-Explainable-Customer-Purchase-Intention-Prediction"), item("Permanent application URL: https://purchase-intention-agent.vercel.app"), item("General project report PDF included in docs/purchase_intention_project_report.pdf"), item("IEEE paper PDF included in docs/ieee_purchase_intention_paper.pdf"), item("This checklist included in docs/ieee_2026_purchase_intention_checklist.pdf"), item("PDFs open correctly and direct download links have been tested")]),
        Paragraph("H. REVIEWER SIGN-OFF", STYLES["SectionBlue"]),
        checklist_table([item("The reviewer can reproduce the local test and training workflow"), item("The reviewer can access the hosted login page and observe the protected workspace"), item("The reviewer understands the difference between local trained inference and hosted lightweight inference"), item("The reviewer accepts the stated limitations and required future work")]),
        Spacer(1, 7 * mm),
        Paragraph("Reviewer comments: ____________________________________________________________________________________________", STYLES["Intro"]),
        Paragraph("____________________________________________________________________________________________________________", STYLES["Intro"]),
        Paragraph("Reviewer signature: ____________________________________________   Date: ____________________", STYLES["Intro"]),
        Spacer(1, 6 * mm),
        Paragraph("Submission status:   [ ] Draft     [ ] Internal review     [ ] Ready for submission     [ ] Revision required", STYLES["Intro"]),
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_checklist()