from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional, List

class MetaInfo(BaseModel):
    urgency: Literal["high", "medium", "low"]
    sentiment: Literal["bullish", "bearish", "neutral"]
    requires_fact_check: bool

class Content(BaseModel):
    headline: str = Field(..., max_length=80)
    body: str = Field(..., max_length=3500)
    tickers: List[str] = Field(default_factory=list)
    media_suggestion: Optional[str] = None

    @field_validator("tickers")
    @classmethod
    def normalize_tickers(cls, v: List[str]):
        return [t if t.startswith("$") else f"${t.upper()}" for t in v]

class Engagement(BaseModel):
    cta_text: str
    suggested_hashtags: List[str]
    best_posting_time_utc: str

class CryptoPostSchema(BaseModel):
    meta: MetaInfo
    content: Content
    engagement: Engagement
    sources: List[str]
    approval_status: Literal["ready_for_review", "needs_edit", "rejected"]
    reasoning: str = Field(..., max_length=300)

    @field_validator("sources")
    @classmethod
    def validate_sources(cls, v):
        if v and not all(s.startswith(("http://", "https://")) for s in v):
            raise ValueError("Sources must be valid URLs")
        return v