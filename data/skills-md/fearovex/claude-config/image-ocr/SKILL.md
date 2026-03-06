---
name: image-ocr
description: >
  Expert in extracting text from images using Tesseract, EasyOCR, PaddleOCR, Google Vision, AWS Textract, Claude Vision.
  Trigger: When extracting text from images, screenshots, scanned documents, or PDFs.
format: reference
---

# Image OCR Expert

> Expert in extracting, processing, and structuring text from images using OCR tools and techniques.

## Description

This skill provides specialized knowledge for extracting text from images, including:
- Tool and library selection by use case (Tesseract, EasyOCR, PaddleOCR, cloud APIs)
- Image preprocessing to maximize OCR accuracy
- Post-processing and structuring of extracted text
- Handling handwriting, receipts, invoices, documents, screenshots
- Multilingual OCR and special character support
- Integration into Python/Node.js/cloud pipelines

**Triggers**: ocr, extract text from image, image to text, read text image, optical character recognition, tesseract, easyocr, paddleocr, textract, vision api, document extraction, screenshot text, invoice ocr, receipt ocr, handwriting recognition, image text extraction

---

## Tool Selection Guide

| Tool | Best For | Languages | Accuracy | Cost |
|------|----------|-----------|----------|------|
| **Tesseract** | Local, simple docs, print text | 100+ | Medium | Free |
| **EasyOCR** | Local, photos, multiple scripts | 80+ | High | Free |
| **PaddleOCR** | Local, CJK languages, tables | 80+ | Very High | Free |
| **Google Vision API** | Cloud, complex docs, handwriting | All | Excellent | Pay-per-use |
| **AWS Textract** | Cloud, forms, tables, invoices | Limited | Excellent | Pay-per-use |
| **Azure Computer Vision** | Cloud, general OCR | 164 | Excellent | Pay-per-use |
| **Surya** | Local, multilingual PDFs | 90+ | High | Free |
| **Docling** | Local, PDFs, structured output | Many | High | Free |

### Decision Tree

```
Is accuracy critical and budget available?
├─ YES → Google Vision API or AWS Textract
└─ NO → Local solution
    ├─ CJK (Chinese/Japanese/Korean) or tables? → PaddleOCR
    ├─ General photos or multiple languages? → EasyOCR
    ├─ Simple printed English docs? → Tesseract
    └─ PDF documents with structure? → Docling or Surya
```

---

## Python Implementations

### Tesseract (pytesseract)

```python
import pytesseract
from PIL import Image
import cv2
import numpy as np

def extract_text_tesseract(image_path: str, lang: str = "eng") -> str:
    """Extract text using Tesseract. Best for clean printed documents."""
    image = Image.open(image_path)

    # Config: --psm 6 = assume uniform block of text
    config = "--psm 6 --oem 3"
    text = pytesseract.image_to_string(image, lang=lang, config=config)
    return text.strip()

def extract_with_confidence(image_path: str) -> list[dict]:
    """Extract text with bounding boxes and confidence scores."""
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    results = []
    for i, word in enumerate(data["text"]):
        if word.strip() and int(data["conf"][i]) > 30:
            results.append({
                "text": word,
                "confidence": data["conf"][i],
                "bbox": {
                    "x": data["left"][i],
                    "y": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i],
                }
            })
    return results

# Install: pip install pytesseract pillow
# System: apt install tesseract-ocr (Linux) / brew install tesseract (Mac)
```

### EasyOCR

```python
import easyocr
from pathlib import Path

def extract_text_easyocr(
    image_path: str,
    languages: list[str] = ["en"],
    detail: bool = False
) -> str | list:
    """
    Extract text using EasyOCR. Best for photos and multiple languages.
    languages: ['en'], ['en', 'es'], ['ch_sim', 'en'], etc.
    """
    reader = easyocr.Reader(languages, gpu=False)  # gpu=True if CUDA available
    results = reader.readtext(image_path)

    if not detail:
        # Return plain text sorted by vertical position
        results_sorted = sorted(results, key=lambda x: x[0][0][1])
        return "\n".join([text for _, text, conf in results_sorted if conf > 0.3])

    return [
        {
            "text": text,
            "confidence": round(conf, 3),
            "bbox": bbox,
        }
        for bbox, text, conf in results
    ]

# Install: pip install easyocr
```

### PaddleOCR (best for CJK and tables)

```python
from paddleocr import PaddleOCR
import json

def extract_text_paddle(
    image_path: str,
    lang: str = "en",  # "en", "ch", "japan", "korean", "es", etc.
    use_angle_cls: bool = True,
) -> str:
    """Extract text using PaddleOCR. Best for CJK and structured documents."""
    ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, show_log=False)
    result = ocr.ocr(image_path, cls=True)

    lines = []
    if result and result[0]:
        # Sort by y position (top to bottom)
        items = sorted(result[0], key=lambda x: x[0][0][1])
        lines = [item[1][0] for item in items if item[1][1] > 0.3]

    return "\n".join(lines)

# Install: pip install paddlepaddle paddleocr
```

### Google Vision API

```python
from google.cloud import vision
import io

def extract_text_google_vision(image_path: str) -> dict:
    """
    Extract text using Google Vision API.
    Requires: GOOGLE_APPLICATION_CREDENTIALS env var set.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Full text detection (better for documents)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    return {
        "text": document.text,
        "pages": [
            {
                "blocks": [
                    {
                        "text": " ".join(
                            symbol.text
                            for para in block.paragraphs
                            for word in para.words
                            for symbol in word.symbols
                        ),
                        "confidence": block.confidence,
                    }
                    for block in page.blocks
                ]
            }
            for page in document.pages
        ]
    }

# Install: pip install google-cloud-vision
```

### AWS Textract (best for forms and invoices)

```python
import boto3
import json

def extract_text_textract(image_path: str, region: str = "us-east-1") -> dict:
    """
    Extract text, forms, and tables using AWS Textract.
    Handles key-value pairs and structured tables automatically.
    """
    client = boto3.client("textract", region_name=region)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["TABLES", "FORMS"]
    )

    # Extract raw text
    blocks = response["Blocks"]
    lines = [b["Text"] for b in blocks if b["BlockType"] == "LINE"]

    # Extract key-value pairs (forms)
    key_values = {}
    key_map = {b["Id"]: b for b in blocks if b["BlockType"] == "KEY_VALUE_SET" and "KEY" in b.get("EntityTypes", [])}
    value_map = {b["Id"]: b for b in blocks if b["BlockType"] == "KEY_VALUE_SET" and "VALUE" in b.get("EntityTypes", [])}

    for key_block in key_map.values():
        key_text = _get_text_from_block(key_block, blocks)
        for rel in key_block.get("Relationships", []):
            if rel["Type"] == "VALUE":
                for val_id in rel["Ids"]:
                    if val_id in value_map:
                        val_text = _get_text_from_block(value_map[val_id], blocks)
                        key_values[key_text] = val_text

    return {
        "text": "\n".join(lines),
        "form_fields": key_values,
    }

def _get_text_from_block(block, all_blocks):
    word_ids = []
    for rel in block.get("Relationships", []):
        if rel["Type"] == "CHILD":
            word_ids.extend(rel["Ids"])

    block_map = {b["Id"]: b for b in all_blocks}
    words = [block_map[wid]["Text"] for wid in word_ids if wid in block_map and block_map[wid]["BlockType"] == "WORD"]
    return " ".join(words)

# Install: pip install boto3
```

---

## Image Preprocessing

Preprocessing is the #1 factor in OCR accuracy. Always apply before running OCR.

```python
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_for_ocr(image_path: str, output_path: str = None) -> np.ndarray:
    """
    Full preprocessing pipeline for maximum OCR accuracy.
    Apply selectively based on image type.
    """
    img = cv2.imread(image_path)

    # 1. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Resize if too small (OCR works better at 300+ DPI)
    height, width = gray.shape
    if width < 1000:
        scale = 2000 / width
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # 3. Deskew (fix rotation)
    gray = deskew(gray)

    # 4. Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # 5. Binarization (choose one based on lighting)
    # Option A: Otsu (uniform lighting)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Option B: Adaptive (uneven lighting, shadows)
    # binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                 cv2.THRESH_BINARY, 11, 2)

    # 6. Morphological cleanup (remove noise dots)
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    if output_path:
        cv2.imwrite(output_path, cleaned)

    return cleaned

def deskew(image: np.ndarray) -> np.ndarray:
    """Correct image rotation using projection analysis."""
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    if abs(angle) < 0.5:  # Skip if nearly straight
        return image

    h, w = image.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)

def enhance_contrast(image_path: str) -> Image.Image:
    """Enhance contrast using PIL - useful for faded text."""
    img = Image.open(image_path).convert("L")
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(2.0)

# Install: pip install opencv-python pillow
```

### Preprocessing Decision Guide

| Image Problem | Solution |
|---------------|----------|
| Rotated/skewed text | `deskew()` |
| Low resolution | Upscale 2x with `cv2.INTER_CUBIC` |
| Uneven lighting/shadows | Adaptive thresholding |
| Uniform background | Otsu thresholding |
| Noisy/grainy | `fastNlMeansDenoising` |
| Faded text | PIL `Contrast` enhancer |
| Color background | Convert to grayscale first |
| Handwriting | Skip binarization, use cloud API |

---

## PDF to Text Extraction

```python
import fitz  # PyMuPDF - for native text extraction
from pdf2image import convert_from_path  # for scanned PDFs
import pytesseract

def extract_pdf_text(pdf_path: str, ocr_fallback: bool = True) -> str:
    """
    Smart PDF extraction:
    - Uses native text layer if available (fast, accurate)
    - Falls back to OCR for scanned pages
    """
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num, page in enumerate(doc):
        # Try native text extraction first
        text = page.get_text().strip()

        if text and len(text) > 50:
            full_text.append(text)
        elif ocr_fallback:
            # Scanned page — render and OCR
            pix = page.get_pixmap(dpi=300)
            img_path = f"/tmp/page_{page_num}.png"
            pix.save(img_path)

            ocr_text = pytesseract.image_to_string(img_path)
            full_text.append(ocr_text)

    doc.close()
    return "\n\n".join(full_text)

# Install: pip install PyMuPDF pdf2image pytesseract
# System: apt install poppler-utils (for pdf2image on Linux)
```

---

## Post-Processing Extracted Text

```python
import re
from difflib import SequenceMatcher

def clean_ocr_text(text: str) -> str:
    """Standard cleanup for OCR output."""
    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n\t]", "", text)

    # Normalize whitespace
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix common OCR misreads
    corrections = {
        r"\b0(?=[a-zA-Z])": "O",    # 0 misread as O before letter
        r"(?<=[a-zA-Z])0\b": "O",    # O misread as 0 after letter
        r"\bl\b": "I",               # lowercase l misread as I (context-dependent)
        r"rn": "m",                  # rn → m (common serif font error)
    }
    for pattern, replacement in corrections.items():
        text = re.sub(pattern, replacement, text)

    return text.strip()

def extract_structured_data(text: str) -> dict:
    """Extract common structured fields from OCR text."""
    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}",
        "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        "amount": r"\$\s?\d+(?:,\d{3})*(?:\.\d{2})?",
        "url": r"https?://[^\s]+",
    }

    return {
        field: re.findall(pattern, text)
        for field, pattern in patterns.items()
    }

def merge_multiline_words(text: str) -> str:
    """Fix hyphenated words split across lines (common in PDFs)."""
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)
```

---

## Node.js / TypeScript

```typescript
// Using Tesseract.js (pure JS, no native deps needed)
import Tesseract from "tesseract.js";

async function extractText(imagePath: string, lang = "eng"): Promise<string> {
  const { data } = await Tesseract.recognize(imagePath, lang, {
    logger: () => {}, // suppress progress logs
  });
  return data.text.trim();
}

// With confidence filtering
async function extractWithConfidence(imagePath: string) {
  const { data } = await Tesseract.recognize(imagePath, "eng");

  return data.words
    .filter((word) => word.confidence > 70)
    .map((word) => ({
      text: word.text,
      confidence: word.confidence,
      bbox: word.bbox,
    }));
}

// Install: npm install tesseract.js
```

```typescript
// Using Google Vision API from Node.js
import vision from "@google-cloud/vision";

const client = new vision.ImageAnnotatorClient();

async function extractTextCloud(imagePath: string): Promise<string> {
  const [result] = await client.documentTextDetection(imagePath);
  return result.fullTextAnnotation?.text ?? "";
}

// Install: npm install @google-cloud/vision
```

---

## Claude Vision API for OCR

Use Claude's vision capability when you need structured extraction + understanding:

```python
import anthropic
import base64
from pathlib import Path

def extract_with_claude(image_path: str, instruction: str = None) -> str:
    """
    Use Claude to extract and structure text from an image.
    Best when you need semantic understanding, not just raw text.
    """
    client = anthropic.Anthropic()

    image_data = base64.standard_b64encode(Path(image_path).read_bytes()).decode()
    ext = Path(image_path).suffix.lower()
    media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    media_type = media_types.get(ext, "image/jpeg")

    prompt = instruction or (
        "Extract ALL text from this image exactly as it appears. "
        "Preserve the original structure, line breaks, and formatting. "
        "Return only the extracted text, nothing else."
    )

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    return message.content[0].text

# Example: structured invoice extraction
def extract_invoice(image_path: str) -> dict:
    result = extract_with_claude(
        image_path,
        instruction="""Extract all data from this invoice and return as JSON:
{
  "invoice_number": "",
  "date": "",
  "vendor": {"name": "", "address": "", "email": ""},
  "items": [{"description": "", "quantity": 0, "unit_price": 0, "total": 0}],
  "subtotal": 0,
  "tax": 0,
  "total": 0
}
Return only valid JSON, no explanation."""
    )
    import json
    return json.loads(result)
```

### When to Use Claude vs Traditional OCR

| Scenario | Use Claude | Use Traditional OCR |
|----------|------------|---------------------|
| Extract + understand structure | ✅ | ❌ |
| Invoice/receipt parsing | ✅ | ❌ (Textract is also good) |
| Handwriting with context | ✅ | ❌ |
| Large volume (1000s of images) | ❌ (cost) | ✅ |
| Simple raw text extraction | ❌ (overkill) | ✅ |
| Tables with complex structure | ✅ | PaddleOCR / Textract |
| Real-time / low latency | ❌ | ✅ |

---

## Accuracy Benchmarks by Image Type

| Image Type | Tesseract | EasyOCR | PaddleOCR | Google Vision |
|------------|-----------|---------|-----------|---------------|
| Printed documents (clean) | 95% | 97% | 97% | 99% |
| Screenshots | 90% | 95% | 95% | 98% |
| Photos of documents | 70% | 88% | 90% | 97% |
| Handwriting | 40% | 55% | 55% | 85% |
| Low res / blurry | 45% | 70% | 72% | 80% |
| Receipts / invoices | 75% | 85% | 88% | 97% |
| Chinese/Japanese/Korean | 60%* | 85% | 95% | 99% |

*Requires additional language pack installation

---

## Common Errors and Fixes

### Tesseract returns garbage text
- **Cause**: Image too small or too noisy
- **Fix**: Upscale 2x, apply denoising and binarization

### EasyOCR misses text in columns
- **Cause**: Default layout analysis fails on multi-column
- **Fix**: Crop each column separately and OCR individually

### PaddleOCR slow on CPU
- **Cause**: Large model loaded
- **Fix**: Use `use_gpu=True` if available, or `use_angle_cls=False` for horizontal text

### Bounding boxes don't align with text
- **Cause**: Image was rotated before OCR
- **Fix**: Apply `deskew()` in preprocessing

### Cloud API returns empty for some regions
- **Cause**: Low contrast or very small text
- **Fix**: Preprocess image, increase DPI, crop region of interest

### PDF text layer has wrong encoding
- **Cause**: Non-standard font embedding
- **Fix**: Use `fitz.Page.get_text("rawdict")` to inspect encoding, or skip to OCR fallback

---

## Quick Start Templates

### Minimal local OCR (Python)
```bash
pip install easyocr
python -c "import easyocr; r=easyocr.Reader(['en']); print('\n'.join([t for _,t,c in r.readtext('image.png') if c>0.3]))"
```

### Minimal cloud OCR (Node.js)
```bash
npm install tesseract.js
node -e "const T=require('tesseract.js'); T.recognize('image.png','eng').then(r=>console.log(r.data.text))"
```

### Batch processing pipeline
```python
from pathlib import Path
import easyocr

reader = easyocr.Reader(["en"], gpu=False)

def batch_ocr(folder: str, output_folder: str) -> None:
    Path(output_folder).mkdir(exist_ok=True)
    images = list(Path(folder).glob("*.{png,jpg,jpeg,tiff,bmp}"))

    for img_path in images:
        results = reader.readtext(str(img_path))
        text = "\n".join(t for _, t, c in results if c > 0.3)

        out_path = Path(output_folder) / f"{img_path.stem}.txt"
        out_path.write_text(text, encoding="utf-8")
        print(f"✓ {img_path.name} → {out_path.name}")

    print(f"\nProcessed {len(images)} images.")

batch_ocr("./images", "./output")
```

## Rules

- Select the OCR engine based on the document type and accuracy requirements before writing code: Tesseract for local/offline simple documents, EasyOCR for multilingual handwriting, cloud APIs (Google Vision, AWS Textract) for production accuracy on structured documents
- Image preprocessing (grayscale conversion, binarization, deskew) is required before Tesseract and EasyOCR for non-ideal inputs — skipping it causes significant accuracy degradation
- OCR output must always be treated as unvalidated text — apply post-processing (regex, string normalization) before using extracted values in business logic
- Never pass sensitive document images to cloud OCR APIs without confirming data privacy and compliance requirements with the project owner
- Confidence scores from the OCR engine must be checked; results below the project-defined threshold must be flagged for human review rather than accepted automatically
