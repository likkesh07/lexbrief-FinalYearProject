"""
models/schemas.py — Pydantic request & response models
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ── Enums ──────────────────────────────────────────────────────────────

class DocumentType(str, Enum):
    auto = "auto"
    contract = "contract"
    nda = "nda"
    lease = "lease"
    tos = "tos"
    privacy = "privacy"
    employment = "employment"
    settlement = "settlement"
    ip = "ip"


class SummaryDepth(str, Enum):
    brief = "brief"
    standard = "standard"
    detailed = "detailed"


class RiskLevel(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


# ── Request Models ─────────────────────────────────────────────────────

class AnalyzeOptions(BaseModel):
    doc_type: DocumentType = DocumentType.auto
    depth: SummaryDepth = SummaryDepth.standard
    include_summary: bool = True
    include_parties: bool = True
    include_key_points: bool = True
    include_obligations: bool = True
    include_risks: bool = True
    include_dates: bool = True


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=100_000)
    options: AnalyzeOptions = AnalyzeOptions()


# ── Response Models ────────────────────────────────────────────────────

class Party(BaseModel):
    role: str
    name: str


class ImportantDate(BaseModel):
    label: str
    value: str


class AnalyzeResult(BaseModel):
    document_type: Optional[str] = None
    risk_level: Optional[str] = None
    word_count: int = 0
    executive_summary: Optional[str] = None
    parties: list[Party] = []
    key_points: list[str] = []
    obligations: list[str] = []
    risks: list[str] = []
    important_dates: list[ImportantDate] = []


class AnalyzeResponse(BaseModel):
    success: bool
    data: Optional[AnalyzeResult] = None
    error: Optional[str] = None


class HistoryItem(BaseModel):
    id: str
    doc_type: str
    risk_level: str
    created_at: str
    word_count: int
    text_preview: str
    result: AnalyzeResult


class HistoryResponse(BaseModel):
    success: bool
    data: list[HistoryItem] = []


class DeleteResponse(BaseModel):
    success: bool
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    service: str = "LexBrief API"
