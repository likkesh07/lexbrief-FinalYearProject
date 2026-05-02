"""
services/google_ai_service.py — Google AI integration for legal analysis
"""
import json
import re
import httpx
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
    """Parse Google AI's JSON response into AnalyzeResult."""
    # Strategy 1: Try to parse the entire response as-is
    try:
        data = json.loads(raw)
        return _build_result(data, text)
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Extract content between first { and last }
    first_brace = raw.find("{")
    last_brace = raw.rfind("}")
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_str = raw[first_brace:last_brace + 1]
        try:
            data = json.loads(json_str)
            return _build_result(data, text)
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Use regex to find JSON object
    match = re.search(r'\{[\s\S]*\}', raw)
    if match:
        json_str = match.group()
        try:
            data = json.loads(json_str)
            return _build_result(data, text)
        except json.JSONDecodeError:
            pass
    
    # Strategy 4: Try to fix common JSON issues
    if first_brace != -1 and last_brace != -1:
        json_str = raw[first_brace:last_brace + 1]
        # Fix trailing commas
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
        # Fix unquoted keys
        json_str = re.sub(r'([{,]\s*)(\w+)(\s*:)', r'\1"\2"\3', json_str)
        try:
            data = json.loads(json_str)
            return _build_result(data, text)
        except json.JSONDecodeError:
            pass
    
    # Strategy 5: Try to complete incomplete JSON by adding missing closing braces
    if first_brace != -1:
        json_str = raw[first_brace:]
        # Count opening and closing braces
        open_count = json_str.count('{')
        close_count = json_str.count('}')
        # Add missing closing braces
        if open_count > close_count:
            json_str += '}' * (open_count - close_count)
        try:
            data = json.loads(json_str)
            return _build_result(data, text)
        except json.JSONDecodeError:
            pass
    
    # Strategy 6: Try to fix incomplete strings by truncating at last complete value
    if first_brace != -1:
        json_str = raw[first_brace:]
        # Find the last complete string value
        last_quote = json_str.rfind('"')
        if last_quote > 0:
            # Check if it's a closing quote
            test_str = json_str[:last_quote + 1]
            # Count quotes to see if it's balanced
            quote_count = test_str.count('"')
            if quote_count % 2 == 0:  # Even number of quotes means balanced
                # Try to close the JSON
                open_count = test_str.count('{')
                close_count = test_str.count('}')
                if open_count > close_count:
                    test_str += '}' * (open_count - close_count)
                try:
                    data = json.loads(test_str)
                    return _build_result(data, text)
                except json.JSONDecodeError:
                    pass
    
    raise ValueError(f"No JSON found in response. Raw response: {raw[:300]}...")


def _build_result(data: dict, text: str) -> AnalyzeResult:
    """Build AnalyzeResult from parsed JSON data."""
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
    Send document to Google AI and return structured analysis.
    """
    settings = get_settings()
    if not settings.google_api_key:
        raise ValueError("Google API key not configured")

    system_prompt = _build_system_prompt(options)
    # Truncate to ~4k chars for faster analysis
    truncated_text = text[:4_000]
    if len(text) > 4_000:
        truncated_text += "\n\n[Document truncated for analysis — showing first 4,000 characters]"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={settings.google_api_key}",
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"{system_prompt}\n\nAnalyze this legal document:\n\n{truncated_text}"
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.1,
                        "maxOutputTokens": 8192,
                    }
                },
                timeout=60.0
            )
            
            response.raise_for_status()
            data = response.json()
            
            if "candidates" not in data or not data["candidates"]:
                raise ValueError("No response from Google AI")
                
            raw_response = data["candidates"][0]["content"]["parts"][0]["text"]
            # Debug: log the full raw response
            print(f"=== Raw AI Response ===")
            print(raw_response)
            print(f"=== End Raw Response ===")
            print(f"Response length: {len(raw_response)}")
            return _parse_response(raw_response, text)
            
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Google AI API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise ValueError(f"Google AI analysis failed: {str(e)}")
