"""
services/anthropic_service.py — Claude AI integration for legal analysis
"""
import json
import re
import anthropic
from models.schemas import AnalyzeOptions, AnalyzeResult, Party, ImportantDate
from config import get_settings


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

    return f"""You are LexBrief, a senior legal analyst AI. Analyze the provided legal document and return structured JSON.

ANALYSIS DEPTH: {depth_guide}
DOCUMENT CONTEXT: {doc_ctx}
REQUESTED SECTIONS: {', '.join(sections)}

Return ONLY a valid JSON object with this exact structure (omit unrequested sections):
{{
  "documentType": "precise document type name",
  "riskLevel": "Low" | "Medium" | "High",
  "wordCount": <integer>,
  "executiveSummary": "2-4 sentence plain English overview of the entire document",
  "parties": [
    {{"role": "Party role (e.g. Employer, Tenant, Licensor)", "name": "Actual party name or 'Not specified'"}}
  ],
  "keyPoints": [
    "Key clause or provision explained in plain English"
  ],
  "obligations": [
    "Specific duty or obligation — who must do what"
  ],
  "risks": [
    "Potential risk or unfavorable clause — explain impact"
  ],
  "importantDates": [
    {{"label": "Date category", "value": "Date, duration, or deadline"}}
  ]
}}

Rules:
- Use plain English in all explanations
- Be specific about clause numbers or sections when visible
- Risk level: High = significant exposure/unfair terms, Medium = standard risks, Low = favorable/balanced
- Return ONLY the JSON, no markdown fences, no preamble"""


def _parse_response(raw: str, text: str) -> AnalyzeResult:
    """Parse Claude's JSON response into AnalyzeResult."""
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
    Send document to Claude AI and return structured analysis.
    """
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    system_prompt = _build_system_prompt(options)
    # Truncate to ~15k chars to stay within context limits
    truncated_text = text[:15_000]
    if len(text) > 15_000:
        truncated_text += "\n\n[Document truncated for analysis — showing first 15,000 characters]"

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this legal document:\n\n{truncated_text}"
            }
        ],
    )

    raw_response = message.content[0].text
    return _parse_response(raw_response, text)
