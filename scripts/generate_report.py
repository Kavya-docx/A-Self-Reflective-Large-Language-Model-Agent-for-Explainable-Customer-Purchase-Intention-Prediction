from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "purchase_intention_project_report.pdf"


def build_report() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=colors.HexColor("#285D46"), spaceAfter=12))
    styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontSize=12, leading=18, textColor=colors.HexColor("#70867B"), spaceAfter=22))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#276D55"), spaceBefore=16, spaceAfter=8))
    styles.add(ParagraphStyle(name="BodyReport", parent=styles["BodyText"], fontSize=9.5, leading=14, textColor=colors.HexColor("#344D42"), spaceAfter=7))
    styles.add(ParagraphStyle(name="SmallReport", parent=styles["BodyText"], fontSize=8, leading=11, textColor=colors.HexColor("#708278")))
    styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=10, leading=15, textColor=colors.HexColor("#285D46"), backColor=colors.HexColor("#E8F1E7"), borderPadding=10, spaceBefore=8, spaceAfter=10))

    story = [
        Paragraph("Self-Reflective Purchase Intention Agent", styles["ReportTitle"]),
        Paragraph("Technical project report | Generated " + date.today().isoformat(), styles["Subtitle"]),
        Paragraph("An open-source, local-first system for explainable customer purchase-intention prediction, self-reflection, and authenticated deployment.", styles["Callout"]),
        Paragraph("Executive Summary", styles["Section"]),
        Paragraph("This project implements an end-to-end purchase-intention agent without paid APIs or proprietary services. It generates privacy-safe behavioural data for reproducible experimentation, trains a calibrated logistic-regression model, exposes signed feature contributions and counterfactual guidance, and runs a deterministic self-reflection pass before returning a decision.", styles["BodyReport"]),
        Paragraph("The system is available locally through FastAPI and a browser workspace, and is deployed to Vercel through a lightweight pure-Python inference adapter. Credential-based access protects hosted prediction routes with an HTTP-only signed session cookie.", styles["BodyReport"]),
        Paragraph("Project Objectives", styles["Section"]),
        Paragraph("1. Predict whether a customer session is likely to result in a purchase. 2. Make each prediction understandable through signed behavioural factors. 3. Detect low-confidence and boundary cases that deserve human review. 4. Keep the stack free, open source, reproducible, and deployable without secrets in source control.", styles["BodyReport"]),
        Paragraph("System Architecture", styles["Section"]),
        Paragraph("The local research path uses Python, pandas, NumPy, scikit-learn, FastAPI, SQLite, and vanilla HTML/CSS/JavaScript. The Vercel path uses FastAPI, Pydantic, and standard-library Python only, avoiding the serverless function size limit caused by scientific dependencies.", styles["BodyReport"]),
        Table([["Layer", "Responsibility", "Implementation"], ["Data", "Generate and validate behavioural aggregates", "data.py"], ["Model", "Train and persist calibrated classifier", "model.py"], ["Explain", "Expose signed local feature impacts", "explain.py"], ["Reflect", "Assess confidence, quality, and stability", "reflection.py"], ["Serve", "API, auth, UI, and audit records", "api.py / api/index.py"], ["Deploy", "Public production hosting", "Vercel + vercel.json"]], colWidths=[25 * mm, 78 * mm, 65 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#276D55")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("LEADING", (0, 0), (-1, -1), 11), ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#DCE4DC")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8F3")]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])),
        Paragraph("Data and Features", styles["Section"]),
        Paragraph("The reproducible generator creates session-duration, pages-viewed, product-views, cart-additions, prior-purchases, discount usage, device type, traffic source, and returning-customer features. The target is a purchase observed within the chosen session window. The validation layer rejects missing, non-finite, out-of-range, or internally inconsistent inputs.", styles["BodyReport"]),
        Paragraph("Model and Evaluation", styles["Section"]),
        Paragraph("The baseline model is a logistic regression pipeline with standardised numeric features and one-hot encoded categorical features. On the verified 800-sample training run with seed 11, the held-out results were:", styles["BodyReport"]),
        Table([["Metric", "Value", "Interpretation"], ["ROC-AUC", "0.7949", "Useful ranking discrimination"], ["Accuracy", "0.7375", "Correct class decisions at 0.5"], ["Brier score", "0.1801", "Probability calibration error"], ["Test samples", "160", "Held-out evaluation size"]], colWidths=[43 * mm, 28 * mm, 97 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#276D55")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#DCE4DC")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8F3")]), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])),
        PageBreak(),
        Paragraph("Explainability and Self-Reflection", styles["Section"]),
        Paragraph("For each scored session, the agent returns positive and negative feature contributions derived from the transformed model input and learned coefficients. It also returns a risk band, a human-readable summary, and a counterfactual suggestion such as increasing high-intent engagement.", styles["BodyReport"]),
        Paragraph("The reflection pass checks four conditions: behavioural input quality, confidence away from the decision boundary, explanation availability, and boundary stability. Low-confidence or invalid cases are marked for human review rather than presented as certain conclusions.", styles["BodyReport"]),
        Paragraph("Authentication and Privacy", styles["Section"]),
        Paragraph("The hosted app presents a credential login interface. Username, password, and session secret are read from environment variables. Successful login creates an HTTP-only, signed, eight-hour cookie; prediction and metrics endpoints reject unauthenticated requests. The repository does not contain passwords or session secrets.", styles["BodyReport"]),
        Paragraph("The demo uses behavioural aggregates rather than names, emails, addresses, or raw event payloads. Hosted SQLite audit data is written to ephemeral /tmp storage and should be replaced with a durable, access-controlled database for production use.", styles["BodyReport"]),
        Paragraph("Deployment", styles["Section"]),
        Paragraph("Production URL: https://purchase-intention-agent.vercel.app. Vercel hosts the lightweight adapter from api/index.py, while local development retains the full scikit-learn research path. The deployment is configured by vercel.json and requirements.txt.", styles["BodyReport"]),
        Paragraph("Validation and Reproducibility", styles["Section"]),
        Paragraph("The repository test suite passes 3 tests covering model discrimination, explanation/reflection output, input validation, and the local API prediction contract. Additional smoke checks verified the Vercel dashboard, health route, login flow, unauthorized 401 response, and authenticated prediction response.", styles["BodyReport"]),
        Paragraph("API Surface", styles["Section"]),
        Table([["Route", "Purpose", "Access"], ["GET /", "Authenticated workspace shell", "Public shell"], ["POST /login", "Create signed session", "Public"], ["POST /logout", "Clear session", "Public"], ["GET /health", "Service status", "Public"], ["GET /model/metrics", "Model validation metrics", "Authenticated"], ["POST /predict", "Score and explain a session", "Authenticated"]], colWidths=[36 * mm, 92 * mm, 40 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#276D55")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#DCE4DC")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8F3")]), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])),
        Paragraph("Limitations and Next Steps", styles["Section"]),
        Paragraph("The current dataset is synthetic and should not be used to make business decisions without retraining and validating on consented production data. Recommended extensions are temporal and group-aware splits, subgroup calibration, drift monitoring, durable audit storage, human feedback capture, and an optional local Ollama or vLLM explanation writer behind the deterministic contract.", styles["BodyReport"]),
        Spacer(1, 12),
        Paragraph("Generated from the open-source project repository. No proprietary model or paid API is required.", styles["SmallReport"]),
    ]
    document.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build_report()