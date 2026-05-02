"""
routes/history.py — GET /api/history, DELETE /api/history/{id}
Manages analysis history stored in a local JSON file.
"""
from fastapi import APIRouter, HTTPException
from models.schemas import HistoryResponse, DeleteResponse
from config import get_settings
import json
import os

router = APIRouter()


def _load_history() -> list:
    settings = get_settings()
    if not os.path.exists(settings.history_file):
        return []
    try:
        with open(settings.history_file, "r") as f:
            return json.load(f)
    except Exception:
        return []


def _save_history(history: list):
    settings = get_settings()
    with open(settings.history_file, "w") as f:
        json.dump(history, f, indent=2)


@router.get("/history", response_model=HistoryResponse)
async def get_history():
    """Return the last 50 analysis history items."""
    history = _load_history()
    return HistoryResponse(success=True, data=history)


@router.delete("/history/{item_id}", response_model=DeleteResponse)
async def delete_history_item(item_id: str):
    """Delete a specific history item by ID."""
    history = _load_history()
    original_count = len(history)
    history = [h for h in history if h.get("id") != item_id]

    if len(history) == original_count:
        raise HTTPException(status_code=404, detail="History item not found")

    _save_history(history)
    return DeleteResponse(success=True, message="History item deleted")


@router.delete("/history", response_model=DeleteResponse)
async def clear_all_history():
    """Clear all history."""
    _save_history([])
    return DeleteResponse(success=True, message="All history cleared")
