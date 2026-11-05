from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

FEATURES = [
    "session_duration_minutes",
    "pages_viewed",
    "product_views",
    "cart_additions",
    "prior_purchases",
    "discount_used",
    "device_type",
    "traffic_source",
    "returning_customer",
]
NUMERIC_FEATURES = [
    "session_duration_minutes", "pages_viewed", "product_views",
    "cart_additions", "prior_purchases", "discount_used", "returning_customer",
]
CATEGORICAL_FEATURES = ["device_type", "traffic_source"]


@dataclass(frozen=True)
class DatasetBundle:
    frame: pd.DataFrame
    target: pd.Series


def generate_dataset(n_samples: int = 4000, seed: int = 42) -> DatasetBundle:
    """Generate privacy-safe behavioural aggregates with a learnable target."""
    if n_samples < 100:
        raise ValueError("n_samples must be at least 100")
    rng = np.random.default_rng(seed)
    returning = rng.binomial(1, 0.42, n_samples)
    product_views = rng.poisson(3.2 + returning * 1.1, n_samples).clip(0, 20)
    pages = (product_views + rng.poisson(2.5, n_samples) + 1).clip(1, 40)
    duration = (pages * rng.uniform(0.7, 2.4, n_samples) + rng.normal(3, 3, n_samples)).clip(1, 90)
    carts = rng.binomial(np.minimum(product_views, 8), 0.12 + returning * 0.08)
    prior = rng.poisson(0.8 + returning * 1.4, n_samples).clip(0, 15)
    discount = rng.binomial(1, 0.28, n_samples)
    device = rng.choice(["mobile", "desktop", "tablet"], n_samples, p=[0.58, 0.35, 0.07])
    source = rng.choice(["organic", "paid", "email", "social", "direct"], n_samples, p=[.3, .2, .15, .15, .2])
    logit = (-3.2 + 0.07 * duration + 0.08 * pages + 0.28 * product_views +
             0.95 * carts + 0.18 * prior + 0.42 * discount + 0.8 * returning +
             (device == "desktop") * 0.18 + (source == "email") * 0.34 +
             (source == "direct") * 0.16 + rng.normal(0, 0.55, n_samples))
    probability = 1 / (1 + np.exp(-logit))
    target = pd.Series(rng.binomial(1, probability), name="purchase")
    frame = pd.DataFrame({
        "session_duration_minutes": duration.round(2), "pages_viewed": pages,
        "product_views": product_views, "cart_additions": carts,
        "prior_purchases": prior, "discount_used": discount, "device_type": device,
        "traffic_source": source, "returning_customer": returning,
    })
    return DatasetBundle(frame=frame[FEATURES], target=target)


def validate_features(values: dict) -> list[str]:
    errors = []
    for name in NUMERIC_FEATURES:
        if name not in values:
            errors.append(f"missing feature: {name}")
        elif not isinstance(values[name], (int, float)) or not np.isfinite(values[name]):
            errors.append(f"{name} must be a finite number")
    for name, allowed in {"device_type": {"mobile", "desktop", "tablet"}, "traffic_source": {"organic", "paid", "email", "social", "direct"}}.items():
        if values.get(name) not in allowed:
            errors.append(f"{name} must be one of {sorted(allowed)}")
    if values.get("pages_viewed", 0) < values.get("product_views", 0):
        errors.append("pages_viewed should be at least product_views")
    return errors