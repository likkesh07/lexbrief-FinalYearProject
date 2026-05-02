"""
services/ollama_service.py — Ollama AI integration for legal analysis
"""
import json
import re
import ollama
from models.schemas import AnalyzeOptions, AnalyzeResult, Party, ImportantDate


def _build_system_prompt(options: AnalyzeOptions) -> str:
    sections = []
    if options.include_summary:
        sections.append("executiveSummary")
    if options.include_parties:
        sections.append("parties")
    if options.include_key_points:
        sections.append("keyPoints")
    if options.include_obligations:
        sections.append("obligations")
    if options.include_risks:
        sections.append("risks")
    if options.include_dates:
        sections.append("importantDates")

    doc_ctx = "auto-detect the document type" if options.doc_type == "auto" else f"treat as {options.doc_type}"

    depth_guide = {
        "brief":    "Be concise — extract only the most critical points (3-5 per section).",
        "standard": "Provide a balanced analysis (5-8 points per section).",
        "detailed": "Be thorough and comprehensive (8-12 points per section, include nuances).",
    }[options.depth]

    return f"""You are LexBrief, a legal analyst AI. Analyze the document and return JSON.

SECTIONS: {', '.join(sections)}
DEPTH: {depth_guide}
CONTEXT: {doc_ctx}

Return ONLY this JSON structure (omit unrequested sections):
{{
  "documentType": "document type",
  "riskLevel": "Low|Medium|High", 
  "wordCount": <int>,
  "executiveSummary": "2-4 sentence overview",
  "parties": [{{"role": "role", "name": "name"}}],
  "keyPoints": ["key point in plain English"],
  "obligations": ["specific obligation"],
  "risks": ["potential risk"],
  "importantDates": [{{"label": "type", "value": "date"}}]
}}

Rules: plain English, specific clauses, return JSON only."""


def _parse_response(raw: str, text: str) -> AnalyzeResult:
    """Parse Ollama's JSON response into AnalyzeResult."""
    # Strip markdown fences if any
    clean = re.sub(r"```(?:json)?", "", raw).strip()
    # Find first { ... } block
    match = re.search(r'\{[\s\S]*\}', clean)
    if not match:
        raise ValueError("No JSON found in response")

    data = json.loads(match.group())

    parties = [
        Party(role=p.get("role", "Unknown"), name=p.get("name", "Not specified"))
        for p in data.get("parties", [])
    ]
    dates = [
        ImportantDate(label=d.get("label", ""), value=d.get("value", ""))
        for d in data.get("importantDates", [])
    ]

    word_count = data.get("wordCount") or len(text.split())

    return AnalyzeResult(
        document_type=data.get("documentType"),
        risk_level=data.get("riskLevel"),
        word_count=word_count,
        executive_summary=data.get("executiveSummary"),
        parties=parties,
        key_points=data.get("keyPoints", []),
        obligations=data.get("obligations", []),
        risks=data.get("risks", []),
        important_dates=dates,
    )


async def analyze_document(text: str, options: AnalyzeOptions) -> AnalyzeResult:
    """
    Send document to Ollama AI and return structured analysis.
    """
    system_prompt = _build_system_prompt(options)
    # Truncate to ~4k chars for faster analysis
    truncated_text = text[:4_000]
    if len(text) > 4_000:
        truncated_text += "\n\n[Document truncated for analysis — showing first 4,000 characters]"

    try:
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': f"Analyze this legal document:\n\n{truncated_text}"
                }
            ],
            options={
                'temperature': 0.1,  # Lower temperature for faster, more deterministic responses
                'num_predict': 1000,  # Limit response length
                'num_ctx': 2048,     # Smaller context window for speed
            }
        )
        raw_response = response['message']['content']
        return _parse_response(raw_response, text)
    except Exception as e:
        raise ValueError(f"Ollama analysis failed: {str(e)}")
