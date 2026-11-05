# Self-Reflective Purchase Intention Agent

An end-to-end, local-first research project for explainable customer purchase-intention prediction. It uses only free and open-source Python packages and does not require an LLM API key.

## What it does

- Generates a reproducible behavioural dataset when no private dataset is available.
- Trains a calibrated logistic-regression classifier on customer/session features.
- Produces a probability, risk band, signed feature contributions, and a practical counterfactual.
- Runs a self-reflection pass that checks confidence, input quality, explanation consistency, and whether the decision is close to the classification boundary.
- Persists model metadata and prediction audit records in SQLite.
- Serves a JSON API and a small browser dashboard.

The self-reflection mechanism is deliberately auditable rather than pretending that an opaque LLM is required: every statement is derived from measurable model outputs. An open-source local LLM can be added later behind the same agent interface, but the baseline remains deterministic and usable offline.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
uvicorn purchase_intention.api:app --reload
```

Open http://127.0.0.1:8000. The first request trains the model and creates `data/purchase_intention.db`.

## Deploy to Vercel

The repository includes `api/index.py`, `requirements.txt`, and `vercel.json` for Vercel's Python runtime. The hosted function uses a lightweight pure-Python inference adapter so it stays below Vercel's function-size limit; local training and research workflows continue to use the full scikit-learn model. From an authenticated machine with the Vercel CLI installed:

```bash
npx vercel login
npx vercel --prod
```

Vercel functions use ephemeral `/tmp` storage, so prediction audit records are not durable there. Use a hosted open-source-compatible PostgreSQL service or self-hosted database for production persistence.

### Credentials

The hosted dashboard is protected by a signed HTTP-only session cookie. Configure these Vercel Production environment variables before sharing the app:

```bash
vercel env add APP_USERNAME production
vercel env add APP_PASSWORD production
vercel env add SESSION_SECRET production
vercel --prod
```

For local development, the fallback credentials are `admin` / `intentlens-demo`. Set the same three environment variables locally to override them. Never commit passwords or session secrets to Git.

To train explicitly:

```bash
python scripts/train.py --samples 5000
```

## API

- `GET /health` - service and model status
- `GET /model/metrics` - validation metrics and feature importance
- `POST /predict` - score one customer/session
- `GET /docs` - generated OpenAPI documentation

Example:

```bash
curl -X POST http://127.0.0.1:8000/predict \
	-H 'content-type: application/json' \
	-d '{"session_duration_minutes": 12, "pages_viewed": 8, "product_views": 4, "cart_additions": 1, "prior_purchases": 2, "discount_used": 0, "device_type":"mobile", "traffic_source":"organic", "returning_customer":1}'
```

## Project layout

```text
src/purchase_intention/
	api.py          FastAPI application and endpoints
	data.py         Synthetic data generation and validation
	explain.py      Local and global model explanations
	model.py        Training, persistence, and inference
	reflection.py   Self-reflection and counterfactual checks
	schemas.py      API contracts
	store.py        SQLite audit persistence
static/index.html Browser dashboard
tests/            Unit and API-level tests
scripts/train.py  Reproducible training entry point
```

## Replacing the demo data

Replace `generate_dataset()` with a loader that maps your consented event data to the feature names in `FEATURES`. Keep the target definition explicit: `purchase` must mean a purchase within the chosen observation window. Do not send personally identifiable information to this service; the current schema intentionally uses behavioural aggregates only.

## Research extensions

1. Compare calibration and subgroup metrics across real cohorts.
2. Add temporal and group-aware train/test splits to prevent leakage.
3. Add drift monitoring and human review feedback to the SQLite store.
4. Put an optional local Ollama/vLLM explanation writer behind the deterministic explanation contract.
