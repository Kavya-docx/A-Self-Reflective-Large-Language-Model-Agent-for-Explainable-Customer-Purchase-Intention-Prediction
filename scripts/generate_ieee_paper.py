from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "ieee_purchase_intention_paper.pdf"


def build_paper() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    margin = 15 * mm
    gap = 6 * mm
    column_width = (width - 2 * margin - gap) / 2
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PaperTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=17, leading=20, alignment=TA_CENTER, spaceAfter=8))
    styles.add(ParagraphStyle(name="Authors", parent=styles["Normal"], fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="Abstract", parent=styles["BodyText"], fontSize=8.5, leading=11, alignment=TA_JUSTIFY, spaceAfter=5))
    styles.add(ParagraphStyle(name="Keywords", parent=styles["BodyText"], fontSize=8.5, leading=11, alignment=TA_JUSTIFY, spaceAfter=8))
    styles.add(ParagraphStyle(name="PaperHeading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=colors.HexColor("#1E4F3A"), spaceBefore=8, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle(name="PaperSubheading", parent=styles["Heading3"], fontName="Helvetica-BoldOblique", fontSize=9, leading=11, spaceBefore=5, spaceAfter=3, keepWithNext=True))
    styles.add(ParagraphStyle(name="PaperBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.2, leading=10.5, alignment=TA_JUSTIFY, spaceAfter=4))
    styles.add(ParagraphStyle(name="PaperRef", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.4, leading=9, leftIndent=8, firstLineIndent=-8, spaceAfter=3))
    styles.add(ParagraphStyle(name="Caption", parent=styles["BodyText"], fontSize=7.2, leading=8.5, alignment=TA_CENTER, textColor=colors.HexColor("#4E6258"), spaceBefore=3, spaceAfter=5))

    title_frame = Frame(margin, margin, width - 2 * margin, height - 2 * margin, id="title")
    left = Frame(margin, margin, column_width, height - 2 * margin, id="left", leftPadding=0, rightPadding=0)
    right = Frame(margin + column_width + gap, margin, column_width, height - 2 * margin, id="right", leftPadding=0, rightPadding=0)

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#6B786F"))
        canvas.drawCentredString(width / 2, 8 * mm, f"Self-Reflective Purchase Intention Agent  |  {document.page}")
        canvas.restoreState()

    document = BaseDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=margin, leftMargin=margin, topMargin=margin, bottomMargin=margin)
    document.addPageTemplates([PageTemplate(id="Title", frames=[title_frame], onPage=footer), PageTemplate(id="TwoColumn", frames=[left, right], onPage=footer)])

    def p(text, style="PaperBody"):
        return Paragraph(text, styles[style])

    story = [
        Paragraph("A Self-Reflective Large Language Model Agent for Explainable Customer Purchase Intention Prediction", styles["PaperTitle"]),
        Paragraph("Open-Source Project Report", styles["Authors"]),
        p("<b>Abstract - </b>This paper presents a local-first agent for explainable customer purchase-intention prediction. The system combines a calibrated logistic-regression model, signed feature contributions, deterministic self-reflection, counterfactual guidance, and credential-protected web deployment. A reproducible synthetic behavioural dataset supports development when private customer data is unavailable. The local research path uses pandas, NumPy, and scikit-learn, while a lightweight pure-Python adapter enables deployment within Vercel serverless size limits. On a held-out evaluation of 160 sessions, the verified model achieved a ROC-AUC of 0.7949, accuracy of 0.7375, and Brier score of 0.1801. The design prioritizes auditability: every decision exposes its evidence, confidence, boundary stability, and recommended next action. The result is a practical foundation for human-supervised purchase-intention analysis rather than an opaque automated decision maker.", "Abstract"),
        p("<b>Index Terms - </b>purchase intention, explainable artificial intelligence, self-reflection, customer behaviour, logistic regression, human-in-the-loop, serverless deployment", "Keywords"),
        PageBreak(),
        p("I. INTRODUCTION", "PaperHeading"),
        p("Predicting whether a customer will purchase is useful for merchandising, personalization, and customer-experience operations. However, a probability without an explanation is difficult to audit and risky to operationalize. This project addresses that gap by treating prediction as a structured decision process with three explicit outputs: purchase intention, decision evidence, and self-reflection."),
        p("The system is designed for constrained and transparent environments. It requires no paid API, proprietary model, or external identity provider. A deterministic baseline provides an inspectable reference point for later experiments with local large language models. The implementation is also deployable: local training uses a conventional scientific Python stack, while the hosted path uses a small inference adapter to satisfy serverless limits."),
        p("The contributions of this work are: (1) a reproducible end-to-end purchase-intention pipeline; (2) model-native local explanations and counterfactual guidance; (3) a self-reflection layer that flags low-confidence cases; and (4) a credential-protected open-source deployment with an explicit three-output API contract."),
        p("II. SYSTEM ARCHITECTURE", "PaperHeading"),
        p("The architecture separates research computation from hosted inference. The data module generates privacy-safe behavioural aggregates and validates incoming sessions. The model module trains a preprocessing and logistic-regression pipeline. The explanation module converts transformed feature values and learned coefficients into signed contributions. The reflection module checks input quality, confidence, explanation availability, and distance from the decision boundary. FastAPI exposes the contract, while SQLite records local audit events."),
        p("For Vercel, the entrypoint in api/index.py avoids pandas, NumPy, SciPy, and scikit-learn. It implements the same behavioural scoring contract with standard-library arithmetic and returns the same prediction, evidence, and reflection structure. This separation is a deployment optimization rather than a claim that the lightweight adapter replaces research validation."),
        p("III. DATA AND FEATURE REPRESENTATION", "PaperHeading"),
        p("The development generator produces session-level features: session duration, pages viewed, product views, cart additions, prior purchases, discount usage, device type, traffic source, and returning-customer status. The target represents a purchase within the selected observation window. Continuous variables are sampled from bounded behavioural distributions, while categorical variables represent common acquisition and device contexts."),
        p("The feature representation intentionally excludes direct identifiers. This is appropriate for a demonstration and creates a clear boundary for future data governance. In a production setting, the target definition, observation window, cohort split, consent status, and retention policy must be documented before training."),
        p("IV. PREDICTION AND EXPLANATION METHOD", "PaperHeading"),
        p("The local classifier is a logistic regression over standardized numeric features and one-hot encoded categorical features. For an input vector x, the purchase probability is computed as:") ,
        p("p(y=1|x) = 1 / (1 + exp(-(w^T x + b)))."),
        p("The local explanation uses the signed contribution c_i = w_i x_i for each transformed feature. Positive contributions increase the log-odds of purchase, while negative contributions decrease them. The API returns the strongest positive and negative factors, preserving direction and magnitude for audit and interface rendering."),
        p("The agent also generates a counterfactual suggestion. If the probability is below the decision threshold, it identifies a small, interpretable engagement change such as additional cart additions or product views. This is guidance for experimentation, not a causal claim."),
        p("V. SELF-REFLECTION AND THREE-OUTPUT CONTRACT", "PaperHeading"),
        p("Self-reflection is implemented as a deterministic verification pass. Input quality checks detect missing, non-finite, or inconsistent values. Confidence is categorized as high, medium, or low according to the distance from p=0.5. Explanation availability and boundary stability are reported independently so consumers can distinguish a strong prediction from a merely available prediction."),
        p("Each successful score returns exactly three typed outputs. Output 1, prediction, contains probability and risk band. Output 2, evidence, contains positive and negative behavioural factors. Output 3, reflection, contains confidence, human-review recommendation, and the next action. Legacy top-level fields remain available for compatibility."),
        p("VI. SECURITY AND DEPLOYMENT", "PaperHeading"),
        p("The hosted interface uses environment-backed username, password, and session-secret values. Successful login creates an HTTP-only, signed, eight-hour cookie. Prediction and metrics routes require a valid session, while health and login remain public. No password or secret is committed to the repository. The demonstration fallback credentials are intended for local evaluation and should be replaced before real use."),
        p("The production application is hosted at purchase-intention-agent.vercel.app. Vercel functions have ephemeral storage, so SQLite audit records written to /tmp are not durable. A production deployment should use a controlled PostgreSQL-compatible store, access logging, rate limiting, secret rotation, and a documented deletion policy."),
        p("VII. EXPERIMENTAL RESULTS", "PaperHeading"),
        p("The verified training run used 800 generated samples and seed 11, with an 80/20 stratified train-test split. The held-out test set contained 160 sessions. Table I reports the observed metrics."),
        Table([["TABLE I\nMETRICS", "VALUE"], ["ROC-AUC", "0.7949"], ["Accuracy", "0.7375"], ["Brier score", "0.1801"], ["Test samples", "160"]], colWidths=[column_width * .68, column_width * .32], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F1E7")), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#BFCFC2")), ("ALIGN", (1, 1), (1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)])),
        p("The metrics demonstrate useful discrimination for a reproducible baseline, but they do not establish production readiness. Because the data is synthetic, performance is primarily a pipeline verification signal. Real evaluation should include temporal splits, subgroup calibration, confidence intervals, drift checks, and comparison against operational baselines."),
        p("VIII. LIMITATIONS AND FUTURE WORK", "PaperHeading"),
        p("The current system does not infer causality, does not model sequence order, and does not include fairness or subgroup analysis. Synthetic data can encode convenient relationships that do not survive contact with real customer behaviour. The serverless adapter is intentionally lightweight and should be evaluated against the trained model on representative cases before being used as a decision service."),
        p("Future work includes group-aware temporal validation, calibration curves, drift monitoring, durable audit storage, human feedback loops, and an optional local Ollama or vLLM explanation writer constrained by the existing deterministic output schema. These extensions preserve the core principle that model uncertainty and evidence should remain visible to the decision maker."),
        p("IX. CONCLUSION", "PaperHeading"),
        p("This project demonstrates an explainable purchase-intention agent that is reproducible, deployable, and explicit about uncertainty. Its most important design choice is to make the output contract understandable: intention, evidence, and reflection are returned together. This creates a practical bridge between machine learning prediction and human-supervised customer decision workflows."),
        p("REFERENCES", "PaperHeading"),
        p("[1] T. Hastie, R. Tibshirani, and J. Friedman, The Elements of Statistical Learning, 2nd ed. Springer, 2009.", "PaperRef"),
        p("[2] M. T. Ribeiro, S. Singh, and C. Guestrin, \"Why should I trust you? Explaining the predictions of any classifier,\" in Proc. ACM SIGKDD, 2016, pp. 1135-1144.", "PaperRef"),
        p("[3] S. Lundberg and S.-I. Lee, \"A unified approach to interpreting model predictions,\" in Proc. NeurIPS, 2017.", "PaperRef"),
        p("[4] FastAPI Documentation, \"FastAPI framework,\" open-source project documentation.", "PaperRef"),
        p("[5] scikit-learn Developers, \"scikit-learn: Machine Learning in Python,\" open-source project documentation.", "PaperRef"),
    ]
    document.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build_paper()