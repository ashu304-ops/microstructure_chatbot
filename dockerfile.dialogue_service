FROM python:3.9-slim

WORKDIR /app

COPY dialogue_service.py .
COPY mechanical_knowledge.json .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

CMD ["python", "dialogue_service.py"]