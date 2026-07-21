#!/usr/bin/env python3
"""
PDF Text Extractor for the pdf-summarizer skill.

Usage:
    python extract_pdf.py <path_to_pdf> [--ocr]

Outputs structured text to stdout with page markers.
"""

import sys
import os
import argparse
import json


def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2 (pure Python, no system deps)."""
    import PyPDF2

    text_pages = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text_pages.append({"page": i + 1, "text": text.strip()})
    return text_pages, num_pages


def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (better table/layout handling)."""
    import pdfplumber

    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            text_pages.append({"page": i + 1, "text": text.strip()})
    return text_pages, num_pages


def extract_with_ocr(pdf_path):
    """Extract text from scanned/image PDFs using OCR (requires pytesseract + pdf2image)."""
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path(pdf_path)
    text_pages = []
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        text_pages.append({"page": i + 1, "text": text.strip()})
    return text_pages, len(images)


def detect_document_type(text_sample):
    """
    Heuristically detect the document type from the first ~2000 chars.
    Returns a string label.
    """
    sample = text_sample.lower()
    if any(kw in sample for kw in ["abstract", "methodology", "references", "doi:", "journal"]):
        return "Research Paper / Academic Article"
    if any(kw in sample for kw in ["agreement", "whereas", "hereby", "indemnif", "party", "clause", "jurisdiction"]):
        return "Legal Contract / Agreement"
    if any(kw in sample for kw in ["revenue", "earnings", "fiscal year", "quarterly", "balance sheet", "ebitda"]):
        return "Financial Report"
    if any(kw in sample for kw in ["table of contents", "chapter", "installation", "configuration", "user guide", "manual"]):
        return "Technical Manual / Documentation"
    if any(kw in sample for kw in ["policy", "regulation", "section", "subsection", "government", "act of"]):
        return "Government / Policy Document"
    if any(kw in sample for kw in ["executive summary", "recommendation", "findings", "analysis"]):
        return "Business Report"
    return "General Document"


def is_text_empty(text_pages):
    """Check if extracted text is basically empty (scanned PDF)."""
    total_chars = sum(len(p["text"]) for p in text_pages)
    return total_chars < 100


def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--ocr", action="store_true", help="Use OCR for scanned PDFs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    pdf_path = args.pdf_path

    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not pdf_path.lower().endswith(".pdf"):
        print(f"WARNING: File does not have a .pdf extension: {pdf_path}", file=sys.stderr)

    # Try extraction
    text_pages = []
    num_pages = 0
    extraction_method = None

    if args.ocr:
        try:
            print("Attempting OCR extraction...", file=sys.stderr)
            text_pages, num_pages = extract_with_ocr(pdf_path)
            extraction_method = "OCR (pytesseract)"
        except ImportError:
            print("ERROR: OCR libraries not available. Install: pip install pdf2image pytesseract", file=sys.stderr)
            sys.exit(1)
    else:
        # Try pdfplumber first (better quality), fall back to PyPDF2
        try:
            text_pages, num_pages = extract_with_pdfplumber(pdf_path)
            extraction_method = "pdfplumber"
        except ImportError:
            try:
                text_pages, num_pages = extract_with_pypdf2(pdf_path)
                extraction_method = "PyPDF2"
            except ImportError:
                print("ERROR: No PDF library available. Install one of: pip install pdfplumber  OR  pip install PyPDF2", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            # Fall back to PyPDF2
            try:
                text_pages, num_pages = extract_with_pypdf2(pdf_path)
                extraction_method = "PyPDF2 (fallback)"
            except Exception as e2:
                print(f"ERROR: Could not extract text: {e2}", file=sys.stderr)
                sys.exit(1)

    # Check if it's a scanned/image PDF
    if is_text_empty(text_pages) and not args.ocr:
        print("\n⚠️  WARNING: Very little text was extracted. This PDF may be scanned or image-based.", file=sys.stderr)
        print("   Try running again with the --ocr flag if you have pytesseract and pdf2image installed.", file=sys.stderr)
        print("   Alternatively, convert the PDF using Adobe Acrobat or upload to Google Drive first.\n", file=sys.stderr)

    # Build the full text sample for type detection
    full_text_sample = " ".join(p["text"] for p in text_pages[:5])
    doc_type = detect_document_type(full_text_sample)

    if args.json:
        output = {
            "file": os.path.basename(pdf_path),
            "num_pages": num_pages,
            "document_type": doc_type,
            "extraction_method": extraction_method,
            "pages": text_pages,
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"=== PDF EXTRACTION RESULTS ===")
        print(f"File: {os.path.basename(pdf_path)}")
        print(f"Pages: {num_pages}")
        print(f"Detected Type: {doc_type}")
        print(f"Extraction Method: {extraction_method}")
        print("=" * 40)
        print()

        for page_data in text_pages:
            page_num = page_data["page"]
            text = page_data["text"]
            print(f"--- PAGE {page_num} ---")
            if text:
                print(text)
            else:
                print("[No text extracted from this page]")
            print()

        print("=== END OF EXTRACTION ===")


if __name__ == "__main__":
    main()
