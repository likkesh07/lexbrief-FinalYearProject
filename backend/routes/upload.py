"""
routes/upload.py — POST /api/upload
Accepts a file (PDF, DOCX, TXT), extracts text, runs analysis.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from models.schemas import AnalyzeOptions, AnalyzeResponse, HistoryItem, DocumentType, SummaryDepth
from services.google_ai_service import analyze_document
from services.pdf_service import extract_text_from_pdf
from services.docx_service import extract_text_from_docx
from utils.helpers import generate_id, now_iso, truncate_text
from config import get_settings
import json
import os

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}


def _save_to_history(item: HistoryItem):
    settings = get_settings()
    history_file = settings.history_file
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.insert(0, item.model_dump())
    history = history[:50]
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


@router.post("/upload", response_model=AnalyzeResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    doc_type: str = Form("auto"),
    depth: str = Form("standard"),
    include_summary: bool = Form(True),
    include_parties: bool = Form(True),
    include_key_points: bool = Form(True),
    include_obligations: bool = Form(True),
    include_risks: bool = Form(True),
    include_dates: bool = Form(True),
):
    """
    Upload a document file and analyze it.
    Supports PDF, DOCX, DOC, TXT.
    """
    settings = get_settings()

    # Validate file size
    file_bytes = await file.read()
    if len(file_bytes) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB."
        )

    # Determine file extension
    filename = file.filename or ""
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Extract text based on file type
    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(file_bytes)
        elif ext in (".docx", ".doc"):
            text = extract_text_from_docx(file_bytes)
        elif ext == ".txt":
            text = file_bytes.decode("utf-8", errors="replace")
        else:
            raise ValueError("Unsupported file type")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if len(text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail="Extracted text is too short. The document may be empty or image-only."
        )

    # Build options
    options = AnalyzeOptions(
        doc_type=DocumentType(doc_type),
        depth=SummaryDepth(depth),
        include_summary=include_summary,
        include_parties=include_parties,
        include_key_points=include_key_points,
        include_obligations=include_obligations,
        include_risks=include_risks,
        include_dates=include_dates,
    )

    try:
        result = await analyze_document(text, options)

        history_item = HistoryItem(
            id=generate_id(),
            doc_type=result.document_type or "Document",
            risk_level=result.risk_level or "Unknown",
            created_at=now_iso(),
            word_count=result.word_count,
            text_preview=truncate_text(text),
            result=result,
        )
        _save_to_history(history_item)

        return AnalyzeResponse(success=True, data=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
