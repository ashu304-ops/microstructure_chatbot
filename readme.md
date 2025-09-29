
# Dockerized Mechanical Domain Chatbot — Your Engineering Q&A Assistant 🤖⚙️

A **Dockerized microservice web application** designed to answer mechanical engineering questions like *“What is Young’s modulus?”* leveraging **NLP** for intent detection and a knowledge base for accurate responses.

---

## 🚀 Project Overview

The Mechanical Domain Chatbot helps users explore core mechanical engineering concepts (stress, Young’s modulus, thermodynamics) through natural language conversations. The backend is split into independent Flask microservices, each handling distinct tasks like user management, NLP processing, or dialogue generation.

Everything runs in Docker containers, orchestrated by Docker Compose, making setup, scaling, and deployment simple and efficient.

---

## 🏗️ Microservice Architecture

| Service              | Port | Role                                                       | Tech Stack                |
| -------------------- | ---- | ---------------------------------------------------------- | ------------------------- |
| **api_gateway**      | 5000 | Entry point routing user requests to appropriate services  | Flask, HTTP REST API      |
| **user_service**     | 5001 | Manages user data (IDs, preferences)                       | Flask, SQLite             |
| **nlp_service**      | 5002 | Detects user intent using NLP (spaCy en_core_web_sm model) | Flask, spaCy              |
| **dialogue_service** | 5003 | Generates replies from knowledge base, logs conversations  | Flask, SQLite, FuzzyWuzzy |
| **frontend**         | 8000 | React-based user interface for chatting                    | React, HTTP API           |

---

## 🔍 How It Works — Data Flow

1. User interacts with the **frontend** (React app).
2. Messages are sent to **api_gateway** which orchestrates:

   * Calls **nlp_service** to detect intent.
   * Calls **dialogue_service** to generate the appropriate response.
   * Uses **user_service** for user context and data management.
3. Responses are relayed back to the frontend for display.

---

## 🗂️ Project Structure

```
project1/
├── data/                          # SQLite databases storage
│   ├── users.db
│   └── conversations.db
├── en_core_web_sm/                # spaCy NLP model files
├── api_gateway.py
├── dialogue_service.py
├── nlp_service.py
├── user_service.py
├── mechanical_knowledge.json      # Knowledge base of mechanical Q&A
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.*                   # Dockerfiles for each service
├── frontend/                      # React frontend source
└── README.md
```

---

## ⚙️ Prerequisites

* **Docker & Docker Compose** installed
* (Optional) **Python 3.9** for local testing
* (Optional) **Node.js** for frontend development
* Internet connection for initial setup

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd project1
```

### 2. Prepare data directory and databases

```bash
mkdir -p data
chmod 777 data
touch data/users.db data/conversations.db
chmod 666 data/users.db data/conversations.db
```

### 3. Verify spaCy model presence

Ensure the folder `en_core_web_sm/en_core_web_sm-3.8.0` contains model files (`config.cfg`, `meta.json`, `vocab/`).

If missing:

```bash
python3 -m venv env
source env/bin/activate
pip install spacy==3.8.0
python -m spacy download en_core_web_sm
cp -r env/lib/python3.9/site-packages/en_core_web_sm .
```

---

## 🚢 Running the Application

### Build Docker containers

```bash
docker-compose build
```

### Start all services

```bash
docker-compose up
```

Access services at:

* Frontend: [http://localhost:8000](http://localhost:8000)
* API Gateway: [http://localhost:5000](http://localhost:5000)

---

## ✅ Testing the Chatbot

### Test via API (curl)

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"user_id":"user1","message":"What is Young’s modulus?"}' \
http://localhost:5000/chat
```

Expected response:

```json
{
  "response": "Young’s modulus (E) is a measure of a material’s stiffness, defined as the ratio of stress to strain in the linear elastic region. It’s given by E = σ/ε, where σ is stress and ε is strain."
}
```

### Test Frontend

* Open [http://localhost:8000](http://localhost:8000)
* Ask a mechanical engineering question, e.g., “What is Young’s modulus?”
* Get instant, detailed answers!

---

## 🔧 Test Individual Microservices

* **NLP Service**

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"message":"What is Young’s modulus?"}' \
http://localhost:5002/process
```

Expected:

```json
{"intent":"material_query"}
```

* **User Service**

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"user_id":"user1","name":"John","preferences":"mechanical"}' \
http://localhost:5001/user
```

Expected:

```json
{"status":"User created","user_id":"user1"}
```

---

## ⚠️ Troubleshooting Tips

* Ensure Docker daemon is running.
* Verify ports 5000-5003 and 8000 are free.
* Check logs with `docker-compose logs`.
* Confirm spaCy model files exist in `en_core_web_sm`.
* Rebuild containers after dependency or code changes.

---

