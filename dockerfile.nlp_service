FROM python:3.9-slim

WORKDIR /app

COPY nlp_service.py .
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm \
    && python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')"

EXPOSE 5002

CMD ["python", "nlp_service.py"]