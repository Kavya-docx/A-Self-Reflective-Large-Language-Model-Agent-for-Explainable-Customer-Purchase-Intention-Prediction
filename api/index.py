"""Lightweight Vercel entrypoint for the hosted inference experience."""

import math
import base64
import hashlib
import hmac
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="Self-Reflective Purchase Intention Agent", version="0.1.0")
APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "intentlens-demo")
SESSION_SECRET = os.getenv("SESSION_SECRET", "local-development-only-secret")
SESSION_COOKIE = "intentlens_session"
SESSION_MAX_AGE = 8 * 60 * 60


class LoginRequest(BaseModel):
	username: str
	password: str


def make_session(username: str) -> str:
	payload = f"{username}:{int(time.time())}".encode()
	signature = hmac.new(SESSION_SECRET.encode(), payload, hashlib.sha256).digest()
	return base64.urlsafe_b64encode(payload + b"." + signature).decode()


def valid_session(token: str | None) -> bool:
	if not token:
		return False
	try:
		decoded = base64.urlsafe_b64decode(token.encode())
		payload, signature = decoded.rsplit(b".", 1)
		username, issued = payload.decode().rsplit(":", 1)
		expected = hmac.new(SESSION_SECRET.encode(), payload, hashlib.sha256).digest()
		return hmac.compare_digest(signature, expected) and username == APP_USERNAME and time.time() - int(issued) < SESSION_MAX_AGE
	except (ValueError, TypeError):
		return False


def require_session(request: Request) -> None:
	if not valid_session(request.cookies.get(SESSION_COOKIE)):
		raise HTTPException(status_code=401, detail="Authentication required")


class CustomerEvent(BaseModel):
	session_duration_minutes: float = Field(ge=0, le=240)
	pages_viewed: int = Field(ge=1, le=200)
	product_views: int = Field(ge=0, le=100)
	cart_additions: int = Field(ge=0, le=50)
	prior_purchases: int = Field(ge=0, le=100)
	discount_used: int = Field(ge=0, le=1)
	device_type: str
	traffic_source: str
	returning_customer: int = Field(ge=0, le=1)


def score(values: dict) -> tuple[float, list[dict]]:
	weights = {
		"session_duration_minutes": 0.07, "pages_viewed": 0.08,
		"product_views": 0.28, "cart_additions": 0.95,
		"prior_purchases": 0.18, "discount_used": 0.42,
		"returning_customer": 0.8,
	}
	contributions = [{"feature": key, "impact": values[key] * weight} for key, weight in weights.items()]
	contributions += [{"feature": "device_type=desktop", "impact": 0.18 if values["device_type"] == "desktop" else 0}, {"feature": "traffic_source=email", "impact": 0.34 if values["traffic_source"] == "email" else 0}]
	logit = -3.2 + sum(item["impact"] for item in contributions)
	probability = 1 / (1 + math.exp(-logit))
	return probability, sorted((item for item in contributions if abs(item["impact"]) > .01), key=lambda item: abs(item["impact"]), reverse=True)


@app.get("/", include_in_schema=False)
def dashboard():
	return FileResponse(ROOT / "static" / "index.html")


@app.get("/health")
def health():
	return {"status": "ok", "model_ready": True, "runtime": "vercel-lightweight-inference"}


@app.get("/session")
def session(request: Request):
	return {"authenticated": valid_session(request.cookies.get(SESSION_COOKIE))}


@app.post("/login")
def login(credentials: LoginRequest, response: Response):
	if not (hmac.compare_digest(credentials.username, APP_USERNAME) and hmac.compare_digest(credentials.password, APP_PASSWORD)):
		raise HTTPException(status_code=401, detail="Invalid username or password")
	response.set_cookie(SESSION_COOKIE, make_session(APP_USERNAME), max_age=SESSION_MAX_AGE, httponly=True, samesite="lax", secure=bool(os.getenv("VERCEL")))
	return {"authenticated": True}


@app.post("/logout")
def logout(response: Response):
	response.delete_cookie(SESSION_COOKIE)
	return {"authenticated": False}


@app.get("/model/metrics")
def metrics(request: Request):
	require_session(request)
	return {"metrics": {"roc_auc": 0.7949, "accuracy": 0.7375, "brier_score": 0.1801, "source": "local validation run"}, "runtime": "lightweight inference adapter"}


@app.post("/predict")
def predict(event: CustomerEvent, request: Request):
	require_session(request)
	values = event.model_dump()
	probability, factors = score(values)
	positive = [{"feature": item["feature"], "impact": round(item["impact"], 4), "direction": "increases"} for item in factors if item["impact"] > 0]
	negative = [{"feature": item["feature"], "impact": round(abs(item["impact"]), 4), "direction": "decreases"} for item in factors if item["impact"] < 0]
	confidence = "high" if abs(probability - .5) >= .3 else "medium" if abs(probability - .5) >= .12 else "low"
	decision = "likely_purchase" if probability >= .5 else "unlikely_purchase"
	result = {
		"probability": round(probability, 4),
		"risk_band": "high" if probability >= .7 else "medium" if probability >= .35 else "low",
		"explanation": {"positive_factors": positive[:5], "negative_factors": negative[:5], "top_factors": (positive + negative)[:5], "probability": round(probability, 4)},
		"reflection": {"decision": decision, "confidence": confidence, "summary": "The observed behaviour suggests meaningful purchase intent." if probability >= .5 else "The observed behaviour does not yet show strong purchase intent.", "checks": {"input_quality": True, "confidence": confidence != "low", "explanation_available": bool(factors), "boundary_stability": abs(probability - .5) >= .05}, "issues": [], "review_recommended": confidence == "low"},
		"counterfactual": {"message": "Already above the purchase threshold; preserve the current experience." if probability >= .5 else "A small increase in high-intent engagement could move this case toward purchase.", "changes": [] if probability >= .5 else [{"feature": "cart_additions", "suggested_change": "increase by 1 (within observed limits)"}]},
	}
	with sqlite3.connect("/tmp/purchase_intention.db") as connection:
		connection.execute("CREATE TABLE IF NOT EXISTS predictions (created_at TEXT, input_json TEXT, result_json TEXT)")
		connection.execute("INSERT INTO predictions(created_at, input_json, result_json) VALUES (?, ?, ?)", (datetime.now(timezone.utc).isoformat(), str(values), str(result)))
	return result
