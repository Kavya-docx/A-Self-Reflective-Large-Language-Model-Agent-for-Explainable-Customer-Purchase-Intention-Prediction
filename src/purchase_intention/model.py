from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES, DatasetBundle, generate_dataset


class PurchaseModel:
    def __init__(self, pipeline: Pipeline, metrics: dict, feature_names: list[str], coefficients: list[float]):
        self.pipeline, self.metrics = pipeline, metrics
        self.feature_names, self.coefficients = feature_names, coefficients

    @classmethod
    def train(cls, bundle: DatasetBundle | None = None, seed: int = 42) -> "PurchaseModel":
        bundle = bundle or generate_dataset(seed=seed)
        preprocessor = ColumnTransformer([
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ])
        pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", LogisticRegression(max_iter=1000, random_state=seed))])
        x_train, x_test, y_train, y_test = train_test_split(bundle.frame, bundle.target, test_size=.2, stratify=bundle.target, random_state=seed)
        pipeline.fit(x_train, y_train)
        probabilities = pipeline.predict_proba(x_test)[:, 1]
        names = list(pipeline.named_steps["preprocessor"].get_feature_names_out())
        coefficients = pipeline.named_steps["classifier"].coef_[0].tolist()
        metrics = {"roc_auc": round(roc_auc_score(y_test, probabilities), 4), "accuracy": round(accuracy_score(y_test, probabilities >= .5), 4), "brier_score": round(brier_score_loss(y_test, probabilities), 4), "test_samples": len(y_test)}
        return cls(pipeline, metrics, names, coefficients)

    def predict_probability(self, values: dict) -> float:
        return float(self.pipeline.predict_proba(pd.DataFrame([values], columns=FEATURES))[0, 1])

    def save(self, path: str | Path) -> None:
        path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)
        path.with_suffix(".json").write_text(json.dumps({"metrics": self.metrics, "feature_names": self.feature_names, "coefficients": self.coefficients}, indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "PurchaseModel":
        return joblib.load(path)