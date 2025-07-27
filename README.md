# Challenge 1A: PDF Outline Extractor using Machine Learning

## 🔍 Objective

Build a Dockerized, offline-capable solution that extracts structured outlines (headings: H1, H2, H3) from PDF documents using a machine learning model trained on visual and layout features. The output is a JSON file matching the provided schema.

---

##  Directory Structure

```
Challenge_1a/
├── input/                        # Input PDFs (mounted as /app/input)
├── output/                       # Output JSONs (mounted as /app/output)
├── sample_dataset/
│   ├── pdfs/                     # Alternate test PDFs
│   ├── outputs/                  # Sample outputs (optional for local testing)
│   └── schema/
│       └── output_schema.json    # JSON schema to validate outputs
├── my_model.joblib
├── my_encoder.joblib
├── process_pdfs.py              # Main PDF processing script
├── validate_output.py           # Output schema validation script
├── Dockerfile
└── README.md
```

---

##  Machine Learning Model

- **Model Type**: RandomForestClassifier (scikit-learn)
- **Features Used**:
  - Font size, bold, italic, centered
  - Capital ratio, font size rank, number of words
  - X-position, presence of digits/colons, heading keywords

- **Model Files**:
  - `my_model.joblib`
  - `my_encoder.joblib`

---

##  Dependencies

- PyMuPDF (fitz)
- pandas
- scikit-learn
- joblib
- jsonschema (for validation)

Install manually (optional for local runs):
```bash
pip install PyMuPDF pandas scikit-learn joblib jsonschema
```

---

##  Running the Solution with Docker

### Step 1: Place your PDFs

Place all test files inside the root-level `input/` directory.

### Step 2: Build the Docker Image

```bash
docker build --platform linux/amd64 -t pdfextractor:omkarbhongale25 .
```

### Step 3: Run the Docker Container

```bash
docker run --rm `
  -v ${PWD}/input:/app/input:ro `
  -v ${PWD}/output:/app/output `
  --network none `
  pdfextractor:omkarbhongale25

```



---

##  Output Format

Each PDF will generate a corresponding `.json` in `/app/output` with this structure:

```json
{
  "title": "filename.pdf",
  "outline": [
    { "level": "H1", "text": "Chapter 1: Introduction", "page": 1 },
    { "level": "H2", "text": "1.1 Background", "page": 2 },
    { "level": "H3", "text": "1.1.1 Early Work", "page": 2 }
  ]
}
```

---

##  Validating Output (Optional)

Run this to verify that the output matches the required schema:

```bash
python validate_output.py
```

> Ensure `output_schema.json` is present at: `sample_dataset/schema/output_schema.json`

---

##  Adobe Challenge Compliance

-  Model size under 200MB
-  CPU-only, Docker-ready
-  No network access required
-  Processes all PDFs from `/app/input`
-  Outputs JSON per PDF in `/app/output`
-  Schema conformance via `output_schema.json`
-  Runs under 60s for 50-page PDFs

---

##  Author

Omkar bhongale  
Adobe India Hackathon 2025 — Challenge 1A Submission