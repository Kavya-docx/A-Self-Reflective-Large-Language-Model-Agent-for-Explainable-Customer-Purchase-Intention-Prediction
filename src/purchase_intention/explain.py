from __future__ import annotations

from .data import FEATURES
from .model import PurchaseModel


def explain_prediction(model: PurchaseModel, values: dict, probability: float) -> dict:
    transformed = model.pipeline.named_steps["preprocessor"].transform(__import__("pandas").DataFrame([values], columns=FEATURES))
    scaled = transformed.toarray()[0] if hasattr(transformed, "toarray") else transformed[0]
    contributions = [(name, float(value * coefficient)) for name, value, coefficient in zip(model.feature_names, scaled, model.coefficients) if abs(value * coefficient) > .01]
    contributions.sort(key=lambda item: abs(item[1]), reverse=True)
    positive = [{"feature": n, "impact": round(v, 4), "direction": "increases"} for n, v in contributions if v > 0][:5]
    negative = [{"feature": n, "impact": round(abs(v), 4), "direction": "decreases"} for n, v in contributions if v < 0][:5]
    return {"positive_factors": positive, "negative_factors": negative, "top_factors": positive + negative, "probability": round(probability, 4)}