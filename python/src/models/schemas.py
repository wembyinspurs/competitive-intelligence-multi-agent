"""Pydantic models shared across all agents and the API layer."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_serializer


# 基础模型：统一处理所有datetime字段的序列化
class BaseSchema(BaseModel):
    @field_serializer("*", when_used="always")
    def serialize_all_fields(self, value):
        # 所有datetime字段自动转ISO标准字符串
        if isinstance(value, datetime):
            return value.isoformat()
        return value


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class ChangeType(str, Enum):
    PRICING = "pricing"
    PRODUCT = "product"
    HIRING = "hiring"
    NEWS = "news"
    PATENT = "patent"
    BLOG = "blog"
    OPEN_SOURCE = "open_source"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Monitor Agent models
# ---------------------------------------------------------------------------
class CompetitorChange(BaseSchema):
    competitor: str
    change_type: ChangeType
    title: str
    summary: str
    url: str = ""
    severity: Severity = Severity.MEDIUM
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    raw_data: dict = Field(default_factory=dict)


class MonitorResult(BaseSchema):
    competitor: str
    changes: list[CompetitorChange] = Field(default_factory=list)
    checked_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Research Agent models
# ---------------------------------------------------------------------------
class ResearchInsight(BaseSchema):
    topic: str
    summary: str
    key_findings: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


class ResearchResult(BaseSchema):
    competitor: str
    insights: list[ResearchInsight] = Field(default_factory=list)
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Compare Agent models
# ---------------------------------------------------------------------------
class DimensionScore(BaseSchema):
    dimension: str
    our_score: float = Field(ge=0.0, le=10.0)
    competitor_score: float = Field(ge=0.0, le=10.0)
    notes: str = ""


class ComparisonMatrix(BaseSchema):
    competitor: str
    dimensions: list[DimensionScore] = Field(default_factory=list)
    overall_assessment: str = ""
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Battlecard Agent models
# ---------------------------------------------------------------------------
class Battlecard(BaseSchema):
    competitor: str
    our_strengths: list[str] = Field(default_factory=list)
    our_weaknesses: list[str] = Field(default_factory=list)
    competitor_strengths: list[str] = Field(default_factory=list)
    competitor_weaknesses: list[str] = Field(default_factory=list)
    key_differentiators: list[str] = Field(default_factory=list)
    objection_handling: dict[str, str] = Field(default_factory=dict)
    elevator_pitch: str = ""
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Alert Agent models
# ---------------------------------------------------------------------------
class Alert(BaseSchema):
    competitor: str
    title: str
    message: str
    severity: Severity
    channel: str = "all"
    sent_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Pipeline state (used by LangGraph)
# ---------------------------------------------------------------------------
class CIState(BaseSchema):
    """Top-level state flowing through the LangGraph pipeline."""
    competitor: str
    changes_detected: list[CompetitorChange] = Field(default_factory=list)
    research_results: list[ResearchInsight] = Field(default_factory=list)
    comparison_matrix: Optional[ComparisonMatrix] = None
    battlecard: Optional[Battlecard] = None
    alerts_sent: list[Alert] = Field(default_factory=list)
    quality_score: float = 0.0
    reflexion_count: int = 0
    error: Optional[str] = None