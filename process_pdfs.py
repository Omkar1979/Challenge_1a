import fitz
import pandas as pd
import joblib
import json
import os

MODEL_FILE = "/app/my_model.joblib"
ENCODER_FILE = "/app/my_encoder.joblib"
SOURCE_DIR = "/app/input"
DEST_DIR = "/app/output"
SIZE_LIMIT = 14.0

classifier = joblib.load(MODEL_FILE)
label_mapper = joblib.load(ENCODER_FILE)
column_headers = classifier.feature_names_in_

def build_feature_vector(text, size, bold, center, italic, page_id, x_start):
    length = len(text)
    trimmed = len(text.strip())
    words = len(text.split())
    digits = int(any(char.isdigit() for char in text))
    colon = int(":" in text)
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    common_words = int(any(kw in text.lower() for kw in ['introduction', 'abstract', 'conclusion', 'chapter']))
    all_upper = int(text.isupper())

    size_tier = (
        3 if size >= 22 else
        2 if size >= 18 else
        1 if size >= 14 else
        0
    )

    return [
        size, int(bold), int(center), int(italic), page_id, x_start,
        length, trimmed, words, digits, colon,
        caps_ratio, common_words, all_upper, size_tier
    ]

def analyze_document(pdf_file):
    doc = fitz.open(pdf_file)
    hierarchy = []
    features_list = []
    lines_meta = []

    for page_idx in range(len(doc)):
        current = doc.load_page(page_idx)
        blocks = current.get_text("dict")["blocks"]

        for blk in blocks:
            if "lines" not in blk:
                continue

            for ln in blk["lines"]:
                txt = ""
                fsize = 0
                bold_flag = False
                italic_flag = False
                x_pos = None

                for sp in ln["spans"]:
                    if not txt:
                        x_pos = sp["bbox"][0]

                    txt += sp["text"].strip() + " "
                    if sp["size"] > fsize:
                        fsize = sp["size"]
                    if "bold" in sp["font"].lower():
                        bold_flag = True
                    if "italic" in sp["font"].lower():
                        italic_flag = True

                content = txt.strip()
                if not content or len(content) < 2:
                    continue

                center_flag = abs(x_pos - (current.rect.width / 2)) < 50

                feat_row = build_feature_vector(
                    content, fsize, bold_flag, center_flag, italic_flag,
                    page_idx + 1, x_pos
                )

                features_list.append(feat_row)
                lines_meta.append({
                    "text": content,
                    "page": page_idx + 1,
                    "font_size": fsize,
                })

    if not features_list:
        return {"title": os.path.basename(pdf_file), "outline": []}

    frame = pd.DataFrame(features_list, columns=column_headers)
    predictions = classifier.predict(frame)
    tags = label_mapper.inverse_transform(predictions)

    for label, meta in zip(tags, lines_meta):
        if meta["font_size"] < SIZE_LIMIT:
            continue
        if label != "None":
            hierarchy.append({
                "level": label,
                "text": meta["text"],
                "page": meta["page"]
            })

    return {
        "title": os.path.basename(pdf_file),
        "outline": hierarchy
    }

def process_directory(source, dest):
    os.makedirs(dest, exist_ok=True)
    documents = [f for f in os.listdir(source) if f.lower().endswith(".pdf")]

    if not documents:
        print(" No PDF files found in:", source)
        return

    for name in documents:
        full_path = os.path.join(source, name)
        output = analyze_document(full_path)
        output_file = os.path.splitext(name)[0] + ".json"
        target_path = os.path.join(dest, output_file)

        with open(target_path, "w", encoding="utf-8") as j:
            json.dump(output, j, indent=2)

        print(f" Processed: {name} → {output_file}")

if __name__ == "__main__":
    process_directory(SOURCE_DIR, DEST_DIR)