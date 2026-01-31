---
name: pdf-harvester
description: Extract text and data from PDF documents
---


# PDF Harvester Skill

> Extract and ingest PDF documents into RAG with proper text extraction, table handling, and metadata.

## Overview

PDFs are common for research papers, reports, manuals, and ebooks. This skill covers:
- Text extraction with layout preservation
- Table extraction and conversion to markdown
- Academic paper patterns (abstract, sections, citations)
- OCR for scanned documents
- Multi-page chunking strategies

## Prerequisites

```bash
# Core extraction
pip install pdfplumber pymupdf

# For OCR (scanned documents)
pip install pytesseract pdf2image
# Also need: brew install tesseract poppler (macOS)

# For academic papers
pip install arxiv  # If fetching from arXiv
```

## Extraction Methods

### Method 1: pdfplumber (Recommended)

Best for structured PDFs with tables.

```python
#!/usr/bin/env python3
"""PDF extraction using pdfplumber."""

import pdfplumber
from pathlib import Path
from typing import Dict, List, Optional
import re

def extract_pdf_text(
    pdf_path: str,
    extract_tables: bool = True
) -> Dict:
    """
    Extract text and tables from PDF.

    Args:
        pdf_path: Path to PDF file
        extract_tables: Whether to extract tables separately

    Returns:
        Dict with pages, tables, and metadata
    """
    result = {
        "pages": [],
        "tables": [],
        "metadata": {},
        "total_pages": 0
    }

    with pdfplumber.open(pdf_path) as pdf:
        result["total_pages"] = len(pdf.pages)
        result["metadata"] = pdf.metadata or {}

        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text
            text = page.extract_text() or ""

            result["pages"].append({
                "page_number": page_num,
                "text": text,
                "width": page.width,
                "height": page.height
            })

            # Extract tables
            if extract_tables:
                tables = page.extract_tables()
                for table_num, table in enumerate(tables, 1):
                    if table and len(table) > 0:
                        result["tables"].append({
                            "page_number": page_num,
                            "table_number": table_num,
                            "data": table,
                            "markdown": table_to_markdown(table)
                        })

    return result


def table_to_markdown(table: List[List]) -> str:
    """Convert table data to markdown format."""
    if not table or len(table) == 0:
        return ""

    # Clean cells
    def clean_cell(cell):
        if cell is None:
            return ""
        return str(cell).replace("
", " ").strip()

    # Header row
    headers = [clean_cell(c) for c in table[0]]
    md = "| " + " | ".join(headers) + " |
"
    md += "| " + " | ".join(["---"] * len(headers)) + " |
"

    # Data rows
    for row in table[1:]:
        cells = [clean_cell(c) for c in row]
        # Pad if necessary
        while len(cells) < len(headers):
            cells.append("")
        md += "| " + " | ".join(cells[:len(headers)]) + " |
"

    return md
```

### Method 2: PyMuPDF (fitz)

Faster, better for large PDFs.

```python
#!/usr/bin/env python3
"""PDF extraction using PyMuPDF."""

import fitz  # PyMuPDF
from typing import Dict, List

def extract_with_pymupdf(pdf_path: str) -> Dict:
    """
    Extract text using PyMuPDF.

    Faster than pdfplumber, good for large documents.
    """
    doc = fitz.open(pdf_path)

    result = {
        "pages": [],
        "metadata": doc.metadata,
        "total_pages": len(doc)
    }

    for page_num, page in enumerate(doc, 1):
        # Get text with layout preservation
        text = page.get_text("text")

        # Get text blocks for better structure
        blocks = page.get_text("dict")["blocks"]

        result["pages"].append({
            "page_number": page_num,
            "text": text,
            "blocks": len(blocks)
        })

    doc.close()
    return result


def extract_with_structure(pdf_path: str) -> Dict:
    """Extract with heading detection."""
    doc = fitz.open(pdf_path)

    pages = []
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]

        structured_content = []
        for block in blocks:
            if block["type"] == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"].strip()
                        font_size = span["size"]
                        is_bold = "bold" in span["font"].lower()

                        # Detect headings by font size
                        if font_size > 14 or is_bold:
                            structured_content.append({
                                "type": "heading",
                                "text": text,
                                "size": font_size
                            })
                        else:
                            structured_content.append({
                                "type": "paragraph",
                                "text": text
                            })

        pages.append({
            "page_number": page_num,
            "content": structured_content
        })

    doc.close()
    return {"pages": pages, "total_pages": len(pages)}
```

### Method 3: OCR for Scanned PDFs

```python
#!/usr/bin/env python3
"""OCR extraction for scanned PDFs."""

import pytesseract
from pdf2image import convert_from_path
from typing import Dict, List

def extract_with_ocr(
    pdf_path: str,
    language: str = "eng",
    dpi: int = 300
) -> Dict:
    """
    Extract text from scanned PDF using OCR.

    Args:
        pdf_path: Path to PDF
        language: Tesseract language code
        dpi: Resolution for conversion
    """
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=dpi)

    pages = []
    for page_num, image in enumerate(images, 1):
        # Run OCR
        text = pytesseract.image_to_string(image, lang=language)

        pages.append({
            "page_number": page_num,
            "text": text,
            "ocr": True
        })

    return {
        "pages": pages,
        "total_pages": len(pages),
        "ocr_used": True
    }


def is_scanned_pdf(pdf_path: str) -> bool:
    """Detect if PDF is scanned (image-based)."""
    import fitz

    doc = fitz.open(pdf_path)

    # Check first few pages
    for page in doc[:min(3, len(doc))]:
        text = page.get_text().strip()
        if len(text) > 100:  # Has extractable text
            doc.close()
            return False

    doc.close()
    return True
```

## Chunking Strategies

### Strategy 1: Page-Based

Simple chunking by page boundaries.

```python
def chunk_by_pages(
    extracted: Dict,
    pages_per_chunk: int = 1
) -> List[Dict]:
    """Chunk PDF by page boundaries."""
    chunks = []
    pages = extracted["pages"]

    for i in range(0, len(pages), pages_per_chunk):
        page_group = pages[i:i + pages_per_chunk]

        text = "

".join(p["text"] for p in page_group)

        chunks.append({
            "content": text,
            "page_start": page_group[0]["page_number"],
            "page_end": page_group[-1]["page_number"],
            "chunk_index": len(chunks)
        })

    return chunks
```

### Strategy 2: Section-Based

Chunk by document sections/headings.

```python
def chunk_by_sections(
    extracted: Dict,
    heading_patterns: List[str] = None
) -> List[Dict]:
    """Chunk PDF by section headings."""
    if heading_patterns is None:
        heading_patterns = [
            r'^#+\s',                    # Markdown headings
            r'^\d+\.\s+[A-Z]',           # Numbered sections
            r'^[A-Z][A-Z\s]+$',          # ALL CAPS headings
            r'^(Abstract|Introduction|Conclusion|References)',
        ]

    full_text = "

".join(p["text"] for p in extracted["pages"])

    # Find section boundaries
    sections = []
    current_section = {"title": "Introduction", "content": "", "start_pos": 0}

    lines = full_text.split("
")

    for line in lines:
        is_heading = any(
            re.match(pattern, line.strip())
            for pattern in heading_patterns
        )

        if is_heading and current_section["content"].strip():
            sections.append(current_section)
            current_section = {
                "title": line.strip(),
                "content": "",
                "start_pos": len(sections)
            }
        else:
            current_section["content"] += line + "
"

    # Don't forget last section
    if current_section["content"].strip():
        sections.append(current_section)

    return [
        {
            "content": s["content"].strip(),
            "section": s["title"],
            "chunk_index": i
        }
        for i, s in enumerate(sections)
    ]
```

### Strategy 3: Semantic Paragraphs

Chunk by paragraph with size limits.

```python
def chunk_by_paragraphs(
    extracted: Dict,
    max_chunk_size: int = 500,  # words
    overlap: int = 50
) -> List[Dict]:
    """Chunk by paragraphs with overlap."""
    full_text = "

".join(p["text"] for p in extracted["pages"])

    # Split into paragraphs
    paragraphs = [p.strip() for p in full_text.split("

") if p.strip()]

    chunks = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para.split())

        if current_size + para_size > max_chunk_size and current_chunk:
            # Save current chunk
            chunks.append({
                "content": "

".join(current_chunk),
                "chunk_index": len(chunks),
                "word_count": current_size
            })

            # Start new chunk with overlap
            overlap_text = current_chunk[-1] if current_chunk else ""
            current_chunk = [overlap_text] if overlap_text else []
            current_size = len(overlap_text.split()) if overlap_text else 0

        current_chunk.append(para)
        current_size += para_size

    # Last chunk
    if current_chunk:
        chunks.append({
            "content": "

".join(current_chunk),
            "chunk_index": len(chunks),
            "word_count": current_size
        })

    return chunks
```

## Academic Paper Pattern

Special handling for research papers.

```python
def extract_academic_paper(pdf_path: str) -> Dict:
    """
    Extract academic paper with structure detection.

    Identifies: title, authors, abstract, sections, references
    """
    extracted = extract_pdf_text(pdf_path)
    full_text = "
".join(p["text"] for p in extracted["pages"])

    paper = {
        "title": "",
        "authors": [],
        "abstract": "",
        "sections": [],
        "references": [],
        "tables": extracted["tables"]
    }

    # Title is usually first large text
    lines = full_text.split("
")
    for line in lines[:10]:
        if len(line) > 20 and len(line) < 200:
            paper["title"] = line.strip()
            break

    # Abstract
    abstract_match = re.search(
        r'Abstract[:\s]*
?(.*?)(?=
(?:1\.?\s+)?Introduction|

[A-Z])',
        full_text,
        re.DOTALL | re.IGNORECASE
    )
    if abstract_match:
        paper["abstract"] = abstract_match.group(1).strip()

    # Sections
    section_pattern = r'
(\d+\.?\s+[A-Z][^
]+)
'
    section_matches = re.finditer(section_pattern, full_text)

    section_positions = [(m.group(1), m.start()) for m in section_matches]

    for i, (title, start) in enumerate(section_positions):
        end = section_positions[i+1][1] if i+1 < len(section_positions) else len(full_text)
        content = full_text[start:end]

        paper["sections"].append({
            "title": title.strip(),
            "content": content.strip()
        })

    # References section
    ref_match = re.search(
        r'(?:References|Bibliography)\s*
(.*?)$',
        full_text,
        re.DOTALL | re.IGNORECASE
    )
    if ref_match:
        paper["references_text"] = ref_match.group(1).strip()

    return paper
```

## Full Harvesting Pipeline

```python
#!/usr/bin/env python3
"""Complete PDF harvesting pipeline."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

async def harvest_pdf(
    pdf_path: str,
    collection: str,
    chunk_strategy: str = "paragraphs",  # pages, sections, paragraphs
    is_academic: bool = False,
    use_ocr: bool = False
) -> Dict:
    """
    Harvest a PDF document into RAG.

    Args:
        pdf_path: Path to PDF file
        collection: Target RAG collection
        chunk_strategy: How to chunk the document
        is_academic: Use academic paper extraction
        use_ocr: Force OCR extraction
    """
    path = Path(pdf_path)

    # Check if OCR needed
    if use_ocr or is_scanned_pdf(pdf_path):
        extracted = extract_with_ocr(pdf_path)
    else:
        extracted = extract_pdf_text(pdf_path)

    # Get document metadata
    doc_metadata = {
        "source_type": "pdf",
        "source_path": str(path.absolute()),
        "filename": path.name,
        "total_pages": extracted["total_pages"],
        "harvested_at": datetime.now().isoformat(),
        "pdf_metadata": extracted.get("metadata", {})
    }

    # Academic paper special handling
    if is_academic:
        paper = extract_academic_paper(pdf_path)
        doc_metadata["title"] = paper["title"]
        doc_metadata["abstract"] = paper["abstract"]
        doc_metadata["is_academic"] = True

    # Chunk based on strategy
    if chunk_strategy == "pages":
        chunks = chunk_by_pages(extracted)
    elif chunk_strategy == "sections":
        chunks = chunk_by_sections(extracted)
    else:
        chunks = chunk_by_paragraphs(extracted)

    # Generate document ID from content hash
    content_hash = hashlib.md5(
        "".join(p["text"] for p in extracted["pages"]).encode()
    ).hexdigest()[:12]
    doc_id = f"pdf_{content_hash}"

    # Ingest chunks
    ingested = 0
    for chunk in chunks:
        chunk_metadata = {
            **doc_metadata,
            "chunk_index": chunk["chunk_index"],
            "total_chunks": len(chunks),
        }

        # Add page info if available
        if "page_start" in chunk:
            chunk_metadata["page_start"] = chunk["page_start"]
            chunk_metadata["page_end"] = chunk["page_end"]

        # Add section info if available
        if "section" in chunk:
            chunk_metadata["section"] = chunk["section"]

        await ingest(
            content=chunk["content"],
            collection=collection,
            metadata=chunk_metadata,
            doc_id=f"{doc_id}_chunk_{chunk['chunk_index']}"
        )
        ingested += 1

    # Ingest tables separately
    for table in extracted.get("tables", []):
        table_metadata = {
            **doc_metadata,
            "content_type": "table",
            "page_number": table["page_number"],
            "table_number": table["table_number"]
        }

        await ingest(
            content=table["markdown"],
            collection=collection,
            metadata=table_metadata,
            doc_id=f"{doc_id}_table_{table['page_number']}_{table['table_number']}"
        )

    return {
        "status": "success",
        "filename": path.name,
        "pages": extracted["total_pages"],
        "chunks": ingested,
        "tables": len(extracted.get("tables", [])),
        "collection": collection,
        "doc_id": doc_id
    }


async def harvest_pdf_url(
    url: str,
    collection: str,
    **kwargs
) -> Dict:
    """Download and harvest a PDF from URL."""
    import httpx
    import tempfile

    # Download PDF
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(response.content)
        temp_path = f.name

    try:
        result = await harvest_pdf(temp_path, collection, **kwargs)
        result["source_url"] = url
        return result
    finally:
        Path(temp_path).unlink()  # Clean up
```

## Metadata Schema

```yaml
# PDF chunk metadata
source_type: pdf
source_path: /path/to/document.pdf
source_url: https://... (if downloaded)
filename: document.pdf
total_pages: 45
page_start: 5
page_end: 7
section: "3. Methodology"
chunk_index: 12
total_chunks: 28
harvested_at: "2024-01-01T12:00:00Z"
is_academic: true
title: "Paper Title"
abstract: "Paper abstract..."
content_type: text|table
```

## Usage Examples

```python
# Local PDF
result = await harvest_pdf(
    pdf_path="/path/to/document.pdf",
    collection="research_papers",
    chunk_strategy="sections",
    is_academic=True
)

# PDF from URL
result = await harvest_pdf_url(
    url="https://arxiv.org/pdf/2301.00001.pdf",
    collection="ml_papers",
    is_academic=True
)

# Scanned document
result = await harvest_pdf(
    pdf_path="/path/to/scanned.pdf",
    collection="legacy_docs",
    use_ocr=True
)
```

## Refinement Notes

> Track improvements as you use this skill.

- [ ] Text extraction tested
- [ ] Table extraction working
- [ ] OCR fallback tested
- [ ] Academic paper pattern validated
- [ ] Chunking strategies compared
- [ ] Large PDF handling optimized
