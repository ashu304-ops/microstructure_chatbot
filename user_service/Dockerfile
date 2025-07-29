FROM python:3.9-slim

WORKDIR /app

COPY user_service.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "user_service.py"]