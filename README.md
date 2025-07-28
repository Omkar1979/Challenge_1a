# Challenge 1A: PDF Outline Extractor using Machine Learning

##  Objective

Build a Dockerized, **offline-capable**, and **CPU-only** solution that extracts structured outlines (`H1`, `H2`, `H3`) from PDF documents using a machine learning model trained on visual and layout features. The extracted outline is saved as a JSON file.

---

##  Pipeline Overview

```mermaid
graph TD
    A[Start] --> B{Is it a heading?}
    B -->|Yes| C[H1 / H2 / H3]
    B -->|No| D[Ignore line]
    C --> E[Write to JSON]
    D --> E


---

##  Directory Structure

```
Challenge_1a/
├── input/                         # Input PDFs (mounted as /app/input)
├── output/                        # Output JSONs (mounted as /app/output)
├── model.joblib                   # Trained RandomForest model
├── encoder.joblib                 # LabelEncoder for heading levels
├── process_pdfs.py                # PDF outline extraction script
├── Dockerfile                     # Dockerfile for containerization
├── sample_dataset/
│   ├── pdfs/                      # Optional sample PDFs
│   ├── outputs/                   # Optional sample outputs
│   └── schema/
│       └── output_schema.json     # Output schema definition (optional)
└── README.md
```

---

## Model Information

- **Type**: RandomForestClassifier (from scikit-learn)
- **Input Features**:
  - Font size, bold, italic, centered
  - X/Y position
  - Font size ratio/z-score
  - Character/word counts
  - Capitalization ratio
- **Model Files**:
  - `model.joblib`
  - `encoder.joblib`

---

##  Dependencies

- PyMuPDF (`fitz`)
- pandas
- scikit-learn
- joblib
- jsonschema *(only for optional schema validation)*

> To install locally (optional):
```bash
pip install PyMuPDF pandas scikit-learn joblib jsonschema
```

---

##  Docker Instructions

### 1️⃣ Build the Docker Image

Make sure you are in the `Challenge_1a` folder and run:

```bash
docker build --platform linux/amd64 -t pdfextractor:omkarbhongale25 .
```

### 2️⃣ Run the Container

**For PowerShell (Windows):**
```powershell
docker run --rm `
  -v ${PWD}\input:/app/input:ro `
  -v ${PWD}\output:/app/output `
  --network none `
  pdfextractor:omkarbhongale25
```

**For Linux/macOS (bash):**
```bash
docker run --rm   -v $(pwd)/input:/app/input:ro   -v $(pwd)/output:/app/output   --network none   pdfextractor:omkarbhongale25
```

---

##  Output Format

Each processed PDF creates a `.json` file in `/app/output` with this structure:

```json
{
  "title": "example.pdf",
  "outline": [
    { "level": "H1", "text": "1. Introduction", "page": 1 },
    { "level": "H2", "text": "1.1 Background", "page": 2 },
    { "level": "H3", "text": "1.1.1 Early Work", "page": 2 }
  ]
}
```

---

##  Sample Output

**For `test_pdf.pdf`**:
```json
{
  "title": "test_pdf.pdf",
  "outline": [
    { "level": "H1", "text": "Introduction to AI", "page": 1 },
    { "level": "H2", "text": "1.1 Historical Background", "page": 1 },
    { "level": "H3", "text": "1.1.1 Turing's Contribution", "page": 2 },
    { "level": "H1", "text": "Conclusion", "page": 5 }
  ]
}
```

---

##  Constraints Satisfied

| Constraint                            | Status   |
|--------------------------------------|----------|
| Offline execution                    |  Yes   |
| CPU-only                             |  Yes   |
| Dockerized                           |  Yes   |
| Image size under 1 GB                |  Yes   |
| No internet access (`--network none`)|  Yes   |
| Processes 3–5 PDFs within 60 seconds |  Yes   |
| Outputs structured JSON per PDF      |  Yes   |

---



##  Optional Validation

To verify the generated outputs against the schema:

```bash
python validate_output.py
```

Make sure `output_schema.json` is located at:
```
sample_dataset/schema/output_schema.json
```

---

## 🔮 Future Improvements

- Use `Tesseract OCR` to handle scanned PDFs (image-based)
- Fine-tune model with more samples including:
  - Nested outlines
  - PDFs with tables of contents
- Switch to `LightGBM` or `XGBoost` for smaller model size
-  layout-aware embeddings like `LayoutLM` if GPU allowed

---

## 👨‍💻 Author

**Omkar Bhongale**  
Submission for **Adobe India Hackathon 2025 — Challenge 1A**
