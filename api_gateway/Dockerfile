FROM python:3.9-slim

WORKDIR /app

COPY api_gateway.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "api_gateway.py"]