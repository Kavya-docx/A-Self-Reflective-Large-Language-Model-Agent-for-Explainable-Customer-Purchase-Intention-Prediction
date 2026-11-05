from typing import Literal

from pydantic import BaseModel, Field


class CustomerEvent(BaseModel):
    session_duration_minutes: float = Field(ge=0, le=240)
    pages_viewed: int = Field(ge=1, le=200)
    product_views: int = Field(ge=0, le=100)
    cart_additions: int = Field(ge=0, le=50)
    prior_purchases: int = Field(ge=0, le=100)
    discount_used: int = Field(ge=0, le=1)
    device_type: Literal["mobile", "desktop", "tablet"]
    traffic_source: Literal["organic", "paid", "email", "social", "direct"]
    returning_customer: int = Field(ge=0, le=1)