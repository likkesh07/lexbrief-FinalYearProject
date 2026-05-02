"""
services/pdf_service.py — Extract text from PDF files using PyMuPDF
"""
import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text from a PDF file given its bytes.
    Returns concatenated text from all pages.
    """
    text_parts = []
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(f"[Page {page_num}]\n{page_text.strip()}")
        doc.close()
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {str(e)}")

    if not text_parts:
        raise ValueError(
            "No text could be extracted from this PDF. "
            "It may be a scanned image PDF. Please copy and paste the text manually."
        )

    return "\n\n".join(text_parts)
