Mechanical Domain Chatbot
Welcome to the Mechanical Domain Chatbot! This project is a Dockerized web application that answers questions about mechanical engineering concepts, such as Young’s modulus, stress, and thermodynamics. It uses natural language processing (NLP) to detect user intents and provides responses from a knowledge base. The application is built with Flask microservices and a React frontend, all orchestrated with Docker Compose.
Table of Contents

Overview
Project Structure
Prerequisites
Setup Instructions
Running the Application
Testing the Application
Troubleshooting


Overview
The chatbot consists of five services:

api_gateway: Routes user requests to appropriate services (port 5000).
user_service: Manages user data in an SQLite database (port 5001).
nlp_service: Processes user messages to detect intents using spaCy (port 5002).
dialogue_service: Generates responses based on intents and a knowledge base (port 5003).
frontend: A React interface for users to interact with the chatbot (port 8000).

The services communicate over a Docker network, and data is stored in SQLite databases (users.db and conversations.db) in a shared data directory.
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
Internet access: For downloading dependencies during the initial setup.

Setup Instructions

Clone the Repository:
git clone <repository-url>
cd project1


Create the Data Directory:Create a directory for SQLite database files and set permissions:
mkdir -p data
chmod 777 data
touch data/users.db
touch data/conversations.db
chmod 666 data/users.db
chmod 666 data/conversations.db


Set Up the spaCy Model:The nlp_service requires the en_core_web_sm model for NLP. It’s included in en_core_web_sm/. Verify its contents:
ls -R en_core_web_sm/en_core_web_sm-3.8.0

Ensure config.cfg, meta.json, and vocab/ are present. If missing, install locally:
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





Running the Application

Build and Start Containers:
docker-compose build
docker-compose up

This starts all services:

api_gateway: http://localhost:5000
user_service: http://localhost:5001
nlp_service: http://localhost:5002
dialogue_service: http://localhost:5003
frontend: http://localhost:8000


Check Logs:
docker-compose logs

Look for:

nlp_service: Running on http://0.0.0.0:5002
user_service: Running on http://0.0.0.0:5001
dialogue_service: Running on http://0.0.0.0:5003



Testing the Application

Test the API:Send a chat request:
curl -X POST -H "Content-Type: application/json" -d '{"user_id":"user1","message":"What is Young’s modulus?"}' http://localhost:5000/chat

Expected response:
{"response":"Young’s modulus (E) is a measure of a material’s stiffness, defined as the ratio of stress to strain in the linear elastic region. It’s given by E = σ/ε, where σ is stress and ε is strain."}


Test the Frontend:

Open http://localhost:8000 in a browser.
Type “What is Young’s modulus?” in the chat interface.
Verify the response matches the above.


Test Individual Services:

nlp_service:curl -X POST -H "Content-Type: application/json" -d '{"message":"What is Young’s modulus?"}' http://localhost:5002/process

Expected: {"intent":"material_query"}
user_service:curl -X POST -H "Content-Type: application/json" -d '{"user_id":"user1","name":"John","preferences":"mechanical"}' http://localhost:5001/user





Troubleshooting

nlp_service Error: OSError: [E050] Can't find model 'en_core_web_sm':
Verify en_core_web_sm/en_core_web_sm-3.8.0 contains config.cfg and meta.json.
Rebuild: docker-compose build nlp_service.


Database Error: sqlite3.OperationalError: unable to open database file:
Ensure ~/project1/data exists and is writable: chmod 777 ~/project1/data.
Check volume mounts in docker-compose.yml.


Build Fails:
Clear cache: docker builder prune.
Check logs: cat build.log.


Network Issues:
Configure proxy in ~/.docker/config.json if needed.
Restart Docker: sudo systemctl restart docker.

