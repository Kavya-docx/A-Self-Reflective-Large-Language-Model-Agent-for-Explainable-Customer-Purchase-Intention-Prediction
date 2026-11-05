from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "purchase_intention_project_report.pdf"
BLUE = colors.HexColor("#284C76")
LIGHT_BLUE = colors.HexColor("#E8EEF6")
TEXT = colors.HexColor("#2F4053")
MUTED = colors.HexColor("#647A91")
LINE = colors.HexColor("#D8E0EA")


def table(data, widths, header=True):
    commands = [("GRID", (0, 0), (-1, -1), .35, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("LEADING", (0, 0), (-1, -1), 11), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")])]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE), ("TEXTCOLOR", (0, 0), (-1, 0), BLUE), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
    return Table(data, colWidths=widths, style=TableStyle(commands))


def build_report():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverKicker", parent=styles["Normal"], fontName="Helvetica", fontSize=13, leading=16, alignment=TA_CENTER, textColor=MUTED, spaceAfter=25))
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=29, leading=35, alignment=TA_CENTER, textColor=BLUE, spaceAfter=14))
    styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=12, leading=17, alignment=TA_CENTER, textColor=MUTED, spaceAfter=28))
    styles.add(ParagraphStyle(name="Chapter", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=BLUE, spaceAfter=8))
    styles.add(ParagraphStyle(name="ChapterRule", parent=styles["Normal"], fontSize=9, leading=12, textColor=MUTED, spaceAfter=19))
    styles.add(ParagraphStyle(name="Heading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=BLUE, spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.6, leading=14, alignment=TA_JUSTIFY, textColor=TEXT, spaceAfter=8))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=11, textColor=MUTED))
    styles.add(ParagraphStyle(name="Quote", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=11, leading=16, textColor=BLUE, backColor=LIGHT_BLUE, borderPadding=12, spaceBefore=12, spaceAfter=12))
    styles.add(ParagraphStyle(name="Contents", parent=styles["BodyText"], fontSize=11, leading=23, textColor=TEXT))

    def P(text, style="Body"):
        return Paragraph(text, styles[style])

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 9 * mm, "Self-Reflective Purchase Intention Agent")
        canvas.drawRightString(192 * mm, 9 * mm, f"Project Report  |  {doc.page}")
        canvas.restoreState()

    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm)
    story = []

    # 1. Cover
    story += [Spacer(1, 12 * mm), P("PROJECT REPORT", "CoverKicker"), P("A Self-Reflective Large-Language-Model Agent for Explainable Customer Purchase Intention Prediction", "CoverTitle"), P("A reproducible, explainable, and authenticated machine-learning workspace for customer decision support", "CoverSub"), Spacer(1, 18 * mm)]
    story.append(table([["Project type", "Applied AI / Machine Learning prototype"], ["Core approach", "Behavioural prediction + explanations + self-reflection"], ["API framework", "FastAPI"], ["User interface", "Responsive browser workspace"], ["Programming language", "Python"], ["Deployment", "Vercel production environment"]], [42 * mm, 118 * mm], header=False))
    story += [Spacer(1, 25 * mm), P("Machine Learning  •  Explainable AI  •  Human-supervised Decisions", "CoverSub"), Spacer(1, 20 * mm), P("Prepared from the open-source project repository", "Small"), P("Generated " + date.today().isoformat(), "Small"), PageBreak()]

    # 2. Contents and executive summary
    story += [P("CONTENTS", "Chapter"), P("A structured project report", "ChapterRule"), P("01  Project Overview .................................................... 3", "Contents"), P("02  System Design ........................................................ 4", "Contents"), P("03  Model and Explainability ........................................ 5", "Contents"), P("04  Security and Deployment ........................................ 6", "Contents"), P("05  Results and Conclusion .......................................... 7", "Contents"), Spacer(1, 14 * mm), P("EXECUTIVE SUMMARY", "Heading"), P("This project implements an end-to-end agent for predicting customer purchase intention from behavioural session features. It combines a calibrated logistic-regression model with signed evidence, counterfactual guidance, and a deterministic self-reflection pass. The result is a decision-support system that exposes not only what it predicts, but also why the prediction was made and whether a human should review it.") , P("The project is intentionally local-first and open source. It runs without a paid API or proprietary service, provides a reproducible synthetic dataset for experimentation, and deploys a lightweight inference adapter to Vercel. The hosted workspace uses credential-based access and returns exactly three outputs for each scored session: intention, evidence, and reflection."), P("The current verified model run achieved a ROC-AUC of 0.7949, accuracy of 0.7375, and Brier score of 0.1801 on 160 held-out samples. These results validate the pipeline; they do not replace evaluation on consented production data.", "Quote"), PageBreak()]

    # 3. Overview
    story += [P("01  PROJECT OVERVIEW", "Chapter"), P("Problem statement, objectives, and users", "ChapterRule"), P("Problem Statement", "Heading"), P("Customer purchase-intention systems often reduce a complex behavioural session to a single score. A score without evidence is difficult to audit, difficult to improve, and easy to over-trust. This project addresses the need for a transparent prediction workflow that gives decision makers measurable evidence and an explicit confidence check."), P("Project Objectives", "Heading"), table([["Objective", "Outcome"], ["Predict", "Estimate the likelihood of purchase from session behaviour."], ["Explain", "Expose signed factors that increase or decrease the score."], ["Reflect", "Identify uncertainty, invalid inputs, and boundary cases."], ["Protect", "Require credentials before metrics and predictions are accessible."], ["Deploy", "Provide a free, reproducible production URL and local run path."]], [38 * mm, 122 * mm]), Spacer(1, 8 * mm), P("Intended Users", "Heading"), P("The project is designed for researchers, customer-experience analysts, and engineers who need an inspectable baseline before introducing a more complex model. It is not intended to make irreversible decisions about individuals or to replace human review."), P("Design Principle", "Heading"), P("Every prediction should answer three questions: What is the intention estimate? What behavioural evidence supports it? How certain is the system, and what should happen next?" , "Quote"), PageBreak()]

    # 4. System design
    story += [P("02  SYSTEM DESIGN", "Chapter"), P("From behavioural input to a deployable workspace", "ChapterRule"), P("Architecture", "Heading"), P("The local research path uses Python, pandas, NumPy, scikit-learn, FastAPI, SQLite, and vanilla HTML/CSS/JavaScript. The hosted path uses FastAPI, Pydantic, and standard-library Python to remain below Vercel's serverless function-size limit. Both paths preserve the same three-output contract."), table([["Layer", "Responsibility", "Project surface"], ["Data", "Generate and validate privacy-safe aggregates", "data.py"], ["Model", "Train and persist classifier", "model.py"], ["Explain", "Calculate signed feature contributions", "explain.py"], ["Reflect", "Check confidence and stability", "reflection.py"], ["Serve", "Expose API, authentication, and audit store", "api.py / api/index.py"], ["Interface", "Collect session features and render results", "static/index.html"]], [27 * mm, 92 * mm, 41 * mm]), Spacer(1, 8 * mm), P("End-to-End Flow", "Heading"), P("1. A user signs into the workspace. 2. Session features are validated. 3. The model calculates a purchase probability. 4. Feature contributions are ranked by impact. 5. Reflection checks confidence and data quality. 6. The API returns intention, evidence, and reflection. 7. A local audit record is written to SQLite or ephemeral Vercel storage."), P("Data Features", "Heading"), P("The feature set includes session duration, pages viewed, product views, cart additions, prior purchases, discount usage, device type, traffic source, and returning-customer status. Direct personal identifiers are not part of the demonstration schema."), PageBreak()]

    # 5. Model and explainability
    story += [P("03  MODEL AND EXPLAINABILITY", "Chapter"), P("A measurable baseline with visible reasoning", "ChapterRule"), P("Data Generation", "Heading"), P("When private data is unavailable, the generator produces a reproducible behavioural dataset using a fixed random seed. The target is a purchase observed within the chosen session window. This supports pipeline development while making the limitations of synthetic evaluation explicit."), P("Prediction Model", "Heading"), P("The local model is a logistic-regression pipeline. Numeric inputs are standardized and categorical values are one-hot encoded. For an input vector x, the probability is p(y=1|x) = 1 / (1 + exp(-(wT x + b))). The probability is converted into low, medium, or high risk bands for the interface."), P("Three Outputs", "Heading"), table([["Output", "Returned content"], ["1. Intention", "Purchase probability and risk band."], ["2. Evidence", "Positive and negative behavioural factors."], ["3. Reflection", "Confidence, review flag, and next action."]], [37 * mm, 123 * mm]), Spacer(1, 8 * mm), P("Self-Reflection", "Heading"), P("The reflection layer checks input quality, confidence away from the 0.5 boundary, explanation availability, and boundary stability. A low-confidence case is not presented as a definitive conclusion. Instead, it is marked for human review and accompanied by a practical counterfactual suggestion."), P("Explainability Boundary", "Heading"), P("Feature contributions explain the model's internal score; they do not prove that changing a feature will cause a purchase. The report therefore describes counterfactuals as intervention hypotheses, not causal findings."), PageBreak()]

    # 6. Security and deployment
    story += [P("04  SECURITY AND DEPLOYMENT", "Chapter"), P("Credential protection and production delivery", "ChapterRule"), P("Authentication", "Heading"), P("The hosted dashboard uses environment-backed APP_USERNAME, APP_PASSWORD, and SESSION_SECRET values. Successful login creates an HTTP-only, signed cookie with an eight-hour lifetime. The /predict and /model/metrics routes return 401 without a valid session. Health and login remain public so service availability can be checked."), table([["Control", "Implementation"], ["Credentials", "Read from Vercel environment variables; never committed."], ["Session", "HMAC-signed HTTP-only cookie."], ["Transport", "Secure cookie flag on Vercel HTTPS."], ["Data", "Behavioural aggregates; no direct identifiers."], ["Audit", "SQLite locally; ephemeral /tmp on Vercel."], ["Production gap", "Use durable access-controlled database for real use."]], [42 * mm, 118 * mm]), Spacer(1, 8 * mm), P("Deployment", "Heading"), P("Production URL: https://purchase-intention-agent.vercel.app. The repository includes Vercel configuration, a lightweight Python entrypoint, and a small requirements file. Local research and training continue to use the full scientific Python stack."), P("Operational Note", "Heading"), P("Vercel function storage is ephemeral. A production system should add durable persistence, rate limiting, secret rotation, monitoring, data deletion controls, and an incident response process before handling real customer data." , "Quote"), PageBreak()]

    # 7. Results and conclusion
    story += [P("05  RESULTS AND CONCLUSION", "Chapter"), P("Validation, limitations, and next steps", "ChapterRule"), P("Evaluation Results", "Heading"), P("The verified training run used 800 generated samples with seed 11 and an 80/20 stratified split. The held-out set contained 160 samples."), table([["Metric", "Value", "Meaning"], ["ROC-AUC", "0.7949", "Useful ranking discrimination"], ["Accuracy", "0.7375", "Correct decisions at threshold 0.5"], ["Brier score", "0.1801", "Probability calibration error"], ["Automated tests", "3 passed", "Pipeline and API regression coverage"]], [42 * mm, 29 * mm, 89 * mm]), Spacer(1, 9 * mm), P("Limitations", "Heading"), P("The dataset is synthetic, the baseline is not causal, and subgroup fairness has not yet been evaluated. The serverless adapter should be compared against the full trained model on representative cases. The audit store is not durable in Vercel's ephemeral filesystem."), P("Future Work", "Heading"), P("Recommended extensions include temporal and group-aware splits, subgroup calibration, drift monitoring, durable PostgreSQL storage, human feedback capture, and an optional local Ollama or vLLM explanation writer constrained by the existing deterministic schema."), P("Conclusion", "Heading"), P("This project provides a complete foundation for explainable customer purchase-intention prediction. Its central contribution is not only the probability model, but the decision contract around it: intention, evidence, and reflection are returned together. This keeps the system useful for experimentation while preserving the human judgment needed for responsible customer analytics."), Spacer(1, 16 * mm), P("Project artifacts", "Heading"), P("Live workspace: https://purchase-intention-agent.vercel.app\nTechnical report: docs/purchase_intention_project_report.pdf\nIEEE paper: docs/ieee_purchase_intention_paper.pdf", "Small")]

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_report()
