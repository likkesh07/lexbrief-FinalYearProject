"""
routes/analyze.py — POST /api/analyze
Accepts raw text + options, returns AI analysis result.
"""
from fastapi import APIRouter, HTTPException
from models.schemas import AnalyzeRequest, AnalyzeResponse, HistoryItem
from services.ollama_service import analyze_document
from utils.helpers import generate_id, now_iso, truncate_text
import json
import os
from config import get_settings

router = APIRouter()


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
    # Keep only last 50
    history = history[:50]

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze a legal document text using Ollama AI.
    """
    try:
        result = await analyze_document(request.text, request.options)

        # Save to history
        history_item = HistoryItem(
            id=generate_id(),
            doc_type=result.document_type or "Document",
            risk_level=result.risk_level or "Unknown",
            created_at=now_iso(),
            word_count=result.word_count,
            text_preview=truncate_text(request.text),
            result=result,
        )
        _save_to_history(history_item)

        return AnalyzeResponse(success=True, data=result)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
