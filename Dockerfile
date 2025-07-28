FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app


RUN pip install --no-cache-dir pandas scikit-learn joblib PyMuPDF


COPY model.joblib .
COPY encoder.joblib .
COPY process_pdfs.py .


CMD ["python", "process_pdfs.py"]
