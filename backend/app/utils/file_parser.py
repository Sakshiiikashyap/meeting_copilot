import io
from pypdf import PdfReader
from docx import Document
from fastapi import HTTPException


def parse_txt(contents: bytes) -> str:
    try:
        return contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Could not decode .txt file — please ensure it's UTF-8 encoded.",
        )


def parse_pdf(contents: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(contents))
        text_parts = [page.extract_text() or "" for page in reader.pages]
        full_text = "\n".join(text_parts).strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse PDF: {e}")

    if not full_text:
        raise HTTPException(
            status_code=400,
            detail="No extractable text found in PDF — it may be a scanned image without OCR.",
        )
    return full_text


def parse_docx(contents: bytes) -> str:
    try:
        doc = Document(io.BytesIO(contents))
        full_text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse DOCX: {e}")

    if not full_text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in DOCX file.")
    return full_text


def parse_transcript_file(filename: str, contents: bytes) -> str:
    """
    Single entry point — routes to the correct parser based on file extension.
    This is the ONLY function the router needs to call.
    """
    lower_name = filename.lower()

    if lower_name.endswith(".txt"):
        return parse_txt(contents)
    elif lower_name.endswith(".pdf"):
        return parse_pdf(contents)
    elif lower_name.endswith(".docx"):
        return parse_docx(contents)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a .txt, .pdf, or .docx file.",
        )