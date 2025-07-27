FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY process_pdfs.py .
COPY my_model.joblib .
COPY my_encoder.joblib .

RUN pip install --no-cache-dir pandas scikit-learn joblib PyMuPDF

CMD ["python", "process_pdfs.py"]
