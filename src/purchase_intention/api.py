from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from .data import validate_features
from .explain import explain_prediction
from .model import PurchaseModel
from .reflection import counterfactual, reflect
from .schemas import CustomerEvent
from .store import PredictionStore

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path("/tmp") if os.getenv("VERCEL") else ROOT
MODEL_PATH = RUNTIME_ROOT / "purchase_model.joblib"
model: PurchaseModel | None = None
store = PredictionStore(RUNTIME_ROOT / "purchase_intention.db")
app = FastAPI(title="Self-Reflective Purchase Intention Agent", version="0.1.0")


def get_model() -> PurchaseModel:
    global model
    if model is None:
        model = PurchaseModel.load(MODEL_PATH) if MODEL_PATH.exists() else PurchaseModel.train()
        if not MODEL_PATH.exists():
            model.save(MODEL_PATH)
    return model


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "model_ready": MODEL_PATH.exists() or model is not None}


@app.get("/model/metrics")
def metrics():
    current = get_model()
    return {"metrics": current.metrics, "top_global_features": sorted(zip(current.feature_names, current.coefficients), key=lambda x: abs(x[1]), reverse=True)[:10]}


@app.post("/predict")
def predict(event: CustomerEvent):
    values = event.model_dump()
    errors = validate_features(values)
    if errors:
        return {"error": "invalid behavioural data", "issues": errors}
    current = get_model()
    probability = current.predict_probability(values)
    explanation = explain_prediction(current, values, probability)
    reflection = reflect(values, probability, explanation)
    result = {"probability": round(probability, 4), "risk_band": "high" if probability >= .7 else "medium" if probability >= .35 else "low", "explanation": explanation, "reflection": reflection, "counterfactual": counterfactual(values, probability)}
    store.record(values, result)
    return result