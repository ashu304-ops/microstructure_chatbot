Mechanical Domain Chatbot
Welcome to the Mechanical Domain Chatbot! This project is a Dockerized web application that answers mechanical engineering questions (e.g., “What is Young’s modulus?”) using a microservice architecture. It leverages natural language processing (NLP) to detect user intents and provides responses from a knowledge base. The application is built with Flask microservices, a React frontend, and orchestrated with Docker Compose.
This README.md explains the microservice architecture and provides step-by-step instructions to set up and run the application.
Table of Contents

Overview
Microservice Architecture
Project Structure
Prerequisites
Setup Instructions
Running the Application
Testing the Application
Troubleshooting
Contributing

Overview
The Mechanical Domain Chatbot is designed to answer questions about mechanical engineering concepts like stress, Young’s modulus, and thermodynamics. It uses a microservice architecture where each service handles a specific function (e.g., user management, NLP, dialogue generation). All services run in Docker containers, communicate over a network, and store data in SQLite databases.
Microservice Architecture
The application is split into five independent microservices, each with a specific role:

api_gateway (Port 5000):

Purpose: Acts as the entry point for user requests, routing them to the appropriate microservices (e.g., nlp_service for intent detection, dialogue_service for responses).
Tech: Flask, handles HTTP requests and orchestrates communication.
Interactions: Receives user input via /chat endpoint, forwards to nlp_service for intent, then to dialogue_service for responses, and stores user data via user_service.


user_service (Port 5001):

Purpose: Manages user data (e.g., user ID, name, preferences).
Tech: Flask, SQLite (users.db).
Interactions: Stores/retrieves user data via /user endpoint, used by api_gateway for user context.


nlp_service (Port 5002):

Purpose: Processes user messages to detect intents (e.g., material_query for “What is Young’s modulus?”).
Tech: Flask, spaCy (en_core_web_sm model).
Interactions: Receives messages from api_gateway via /process endpoint, returns detected intent.


dialogue_service (Port 5003):

Purpose: Generates responses based on intents using a knowledge base (mechanical_knowledge.json).
Tech: Flask, SQLite (conversations.db), FuzzyWuzzy for matching.
Interactions: Receives intent and message from api_gateway via /dialogue endpoint, returns responses, logs conversations.


frontend (Port 8000):

Purpose: Provides a user-friendly web interface for interacting with the chatbot.
Tech: React, communicates with api_gateway via HTTP requests.
Interactions: Sends user messages to /chat endpoint and displays responses.



Architecture Diagram
+-------------------+
|     Frontend      |  (React, http://localhost:8000)
|     (Port 8000)   |
+-------------------+
          |
          v
+-------------------+
|    API Gateway    |  (Flask, http://localhost:5000)
|     (Port 5000)   |
+-------------------+
          |
          v
+-------------------+    +-------------------+    +-------------------+
|    User Service   |    |    NLP Service    |    | Dialogue Service  |
| (Flask, Port 5001)|<-->| (Flask, Port 5002)|<-->| (Flask, Port 5003)|
|   SQLite:         |    |   spaCy:          |    |   SQLite:         |
|   users.db        |    |   en_core_web_sm  |    |   conversations.db|
+-------------------+    +-------------------+    +-------------------+


Communication: Services communicate over a Docker network (chatbot_network) using HTTP REST APIs.
Data Storage: users.db and conversations.db are stored in a shared data directory, mounted via Docker volumes.
Scalability: Each service can be scaled independently with Docker Compose.

Project Structure
project1/
├── data/
│   ├── users.db
│   └── conversations.db
├── en_core_web_sm/
│   └── en_core_web_sm-3.8.0/
│       ├── config.cfg
│       ├── meta.json
│       ├── vocab/
│       └── ...
├── api_gateway.py
├── dialogue_service.py
├── nlp_service.py
├── user_service.py
├── mechanical_knowledge.json
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.api_gateway
├── Dockerfile.user_service
├── Dockerfile.nlp_service
├── Dockerfile.dialogue_service
├── Dockerfile.frontend
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
└── README.md

Prerequisites

Docker: Install Docker and Docker Compose.
Linux: sudo apt-get install docker.io docker-compose
Windows/Mac: Install Docker Desktop.


Python 3.9: For local testing (optional).
Node.js: For frontend development (optional).
Internet access: For initial dependency downloads.

Setup Instructions
Follow these steps to set up the project on your machine.

Clone the Repository:
git clone <repository-url>
cd project1


Create the Data Directory:Create a directory for SQLite databases and set permissions:
mkdir -p data
chmod 777 data
touch data/users.db
touch data/conversations.db
chmod 666 data/users.db
chmod 666 data/conversations.db


Set Up the spaCy Model:The nlp_service uses the en_core_web_sm model for NLP, included in en_core_web_sm/. Verify its contents:
ls -R en_core_web_sm/en_core_web_sm-3.8.0

Ensure config.cfg, meta.json, vocab/, etc., are present. If missing, install locally:
python3 -m venv env
source env/bin/activate
pip install spacy==3.8.0
python -m spacy download en_core_web_sm
cp -r env/lib/python3.9/site-packages/en_core_web_sm .


Verify Configuration Files:

requirements.txt:flask==2.3.2
flask-cors==4.0.1
spacy==3.8.0
fuzzywuzzy==0.18.0
python-Levenshtein==0.25.1


mechanical_knowledge.json:[
    {
        "question": "What is Young’s modulus?",
        "answer": "Young’s modulus (E) is a measure of a material’s stiffness, defined as the ratio of stress to strain in the linear elastic region. It’s given by E = σ/ε, where σ is stress and ε is strain.",
        "intents": ["material_query"]
    }
]


docker-compose.yml:services:
  api_gateway:
    build:
      context: .
      dockerfile: Dockerfile.api_gateway
    ports:
      - "5000:5000"
    networks:
      - chatbot_network
    depends_on:
      - user_service
      - nlp_service
      - dialogue_service

  user_service:
    build:
      context: .
      dockerfile: Dockerfile.user_service
    ports:
      - "5001:5001"
    networks:
      - chatbot_network
    volumes:
      - ./data:/app/data
    environment:
      - DB_PATH=/app/data/users.db

  nlp_service:
    build:
      context: .
      dockerfile: Dockerfile.nlp_service
    ports:
      - "5002:5002"
    networks:
      - chatbot_network

  dialogue_service:
    build:
      context: .
      dockerfile: Dockerfile.dialogue_service
    ports:
      - "5003:5003"
    networks:
      - chatbot_network
    volumes:
      - ./data:/app/data
    environment:
      - DB_PATH=/app/data/conversations.db

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8000:8000"
    networks:
      - chatbot_network

networks:
  chatbot_network:
    driver: bridge




Verify Dockerfiles:

Dockerfile.nlp_service:FROM python:3.9-slim
WORKDIR /app
COPY nlp_service.py .
COPY requirements.txt .
COPY en_core_web_sm/en_core_web_sm-3.8.0 /usr/local/lib/python3.9/site-packages/en_core_web_sm
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')"
EXPOSE 5002
CMD ["python", "nlp_service.py"]


Dockerfile.user_service:FROM python:3.9-slim
WORKDIR /app
COPY user_service.py .
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && mkdir -p /app/data \
    && chmod 777 /app/data
EXPOSE 5001
CMD ["python", "user_service.py"]


Dockerfile.dialogue_service:FROM python:3.9-slim
WORKDIR /app
COPY dialogue_service.py .
COPY mechanical_knowledge.json .
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && mkdir -p /app/data \
    && chmod 777 /app/data
EXPOSE 5003
CMD ["python", "dialogue_service.py"]





Running the Application

Build the Containers:
docker-compose build

This builds images for all services, including installing dependencies and copying the en_core_web_sm model for nlp_service.

Start the Containers:
docker-compose up

This starts:

api_gateway: http://localhost:5000
user_service: http://localhost:5001
nlp_service: http://localhost:5002
dialogue_service: http://localhost:5003
frontend: http://localhost:8000


Check Logs:
docker-compose logs

Look for:

nlp_service: Running on http://0.0.0.0:5002 and Model loaded successfully
user_service: Running on http://0.0.0.0:5001
dialogue_service: Running on http://0.0.0.0:5003



Testing the Application

Test the API:
curl -X POST -H "Content-Type: application/json" -d '{"user_id":"user1","message":"What is Young’s modulus?"}' http://localhost:5000/chat

Expected:
{"response":"Young’s modulus (E) is a measure of a material’s stiffness, defined as the ratio of stress to strain in the linear elastic region. It’s given by E = σ/ε, where σ is stress and ε is strain."}


Test the Frontend:

Open http://localhost:8000 in a browser.
Type “What is Young’s modulus?” in the chat interface.
Verify the response matches the above.


Test Individual Services:

nlp_service:curl -X POST -H "Content-Type: application/json" -d '{"message":"What is Young’s modulus?"}' http://localhost:5002/process

Expected: {"intent":"material_query"}
user_service:curl -X POST -H "Content-Type: application/json" -d '{"user_id":"user1","name":"John","preferences":"mechanical"}' http://localhost:5001/user

Expected: {"status":"User created","user_id":"user1"}


