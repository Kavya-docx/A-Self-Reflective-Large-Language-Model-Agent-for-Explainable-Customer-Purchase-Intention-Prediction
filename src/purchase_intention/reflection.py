from __future__ import annotations

from .data import validate_features


def reflect(values: dict, probability: float, explanation: dict) -> dict:
    issues = validate_features(values)
    boundary_distance = abs(probability - .5)
    confidence = "high" if boundary_distance >= .3 else "medium" if boundary_distance >= .12 else "low"
    checks = {
        "input_quality": not issues,
        "confidence": confidence != "low",
        "explanation_available": bool(explanation["top_factors"]),
        "boundary_stability": boundary_distance >= .05,
    }
    if probability >= .5:
        decision, summary = "likely_purchase", "The observed behaviour suggests meaningful purchase intent."
    else:
        decision, summary = "unlikely_purchase", "The observed behaviour does not yet show strong purchase intent."
    if confidence == "low":
        summary += " This case is close to the decision boundary and should be treated cautiously."
    return {"decision": decision, "confidence": confidence, "summary": summary, "checks": checks, "issues": issues, "review_recommended": confidence == "low" or bool(issues)}


def counterfactual(values: dict, probability: float) -> dict:
    if probability >= .5:
        return {"message": "Already above the purchase threshold; preserve the current experience.", "changes": []}
    needed = max(1, round((.5 - probability) * 5))
    return {"message": "A small increase in high-intent engagement could move this case toward purchase.", "changes": [{"feature": "cart_additions", "suggested_change": f"increase by {needed} (within observed limits)"}, {"feature": "product_views", "suggested_change": "increase by 2 through relevant recommendations"}]}