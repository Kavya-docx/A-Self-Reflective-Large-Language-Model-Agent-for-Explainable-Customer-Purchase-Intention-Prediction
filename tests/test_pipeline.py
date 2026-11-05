from fastapi.testclient import TestClient

from purchase_intention.data import generate_dataset, validate_features
from purchase_intention.model import PurchaseModel
from purchase_intention.explain import explain_prediction
from purchase_intention.reflection import reflect
from purchase_intention.api import app


def sample():
    return {"session_duration_minutes": 12, "pages_viewed": 8, "product_views": 4, "cart_additions": 1, "prior_purchases": 2, "discount_used": 0, "device_type": "mobile", "traffic_source": "organic", "returning_customer": 1}


def test_training_produces_discriminating_model():
    model = PurchaseModel.train(generate_dataset(600, 7), 7)
    assert model.metrics["roc_auc"] > .65
    probability = model.predict_probability(sample())
    explanation = explain_prediction(model, sample(), probability)
    assert 0 <= probability <= 1
    assert explanation["top_factors"]
    assert reflect(sample(), probability, explanation)["checks"]["input_quality"]


def test_validation_catches_inconsistent_behaviour():
    values = sample() | {"pages_viewed": 2}
    assert "pages_viewed should be at least product_views" in validate_features(values)


def test_api_predict():
    response = TestClient(app).post("/predict", json=sample())
    assert response.status_code == 200
    body = response.json()
    assert {"probability", "explanation", "reflection", "counterfactual"} <= body.keys()