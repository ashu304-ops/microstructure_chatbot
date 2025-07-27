from flask import Flask, request, jsonify
import sqlite3
import json
import random
from fuzzywuzzy import fuzz

app = Flask(__name__)

def init_db():
    try:
        conn = sqlite3.connect("/app/conversations.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS conversations (user_id TEXT, message TEXT, response TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

try:
    with open("mechanical_knowledge.json", "r") as f:
        knowledge_base = json.load(f)
    print(f"Loaded {len(knowledge_base['questions'])} questions from mechanical_knowledge.json")
except FileNotFoundError:
    print("Error: mechanical_knowledge.json not found")
    knowledge_base = {"questions": []}
except Exception as e:
    print(f"Error loading mechanical_knowledge.json: {str(e)}")
    knowledge_base = {"questions": []}

def get_domain_response(message, intent):
    print(f"Processing message: {message}, intent: {intent}")
    best_match = None
    highest_score = 0
    for item in knowledge_base["questions"]:
        score = fuzz.ratio(message.lower(), item["question"].lower())
        print(f"Question: {item['question']}, Score: {score}")
        if score > highest_score and score > 60:
            highest_score = score
            best_match = item["answer"]
    print(f"Best match: {best_match}")
    return best_match or random.choice([
        "Sorry, I’m not sure about that. Can you clarify your question?",
        "Hmm, that’s an interesting one! Could you provide more details?"
    ])

@app.route("/respond", methods=["POST"])
def respond():
    try:
        data = request.get_json()
        print(f"Received request: {data}")
        user_id = data.get("user_id")
        intent = data.get("intent")
        message = data.get("message")

        if not all([user_id, intent, message]):
            raise ValueError("Missing required fields in request")

        conn = sqlite3.connect("/app/conversations.db")
        c = conn.cursor()
        c.execute("SELECT message, response FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT 3", (user_id,))
        history = c.fetchall()
        print(f"Conversation history: {history}")

        responses = {
            "greeting": ["Hello! Ask me about mechanical engineering topics like stress, thermodynamics, or materials.", "Hi! I’m here to help with mechanical engineering questions.", "Hey, let’s talk mechanics!"],
            "farewell": ["Goodbye! Let me know if you have more mechanical questions!", "See you later!", "Take care!"]
        }

        if intent in ["greeting", "farewell"]:
            response = random.choice(responses.get(intent))
            print(f"Selected greeting/farewell response: {response}")
        elif intent.endswith("_query"):
            response = get_domain_response(message, intent)
            if any("thermodynamic" in h[0].lower() for h in history) and "thermodynamic" in message.lower():
                response += " By the way, want to dive deeper into thermodynamics laws?"
            print(f"Selected domain response: {response}")
        else:
            response = get_domain_response(message, intent)
            print(f"Selected default response: {response}")

        c.execute("INSERT INTO conversations (user_id, message, response) VALUES (?, ?, ?)", (user_id, message, response))
        conn.commit()
        conn.close()
        print("Conversation stored successfully")

        return jsonify({"response": response})
    except Exception as e:
        print(f"Error in respond: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5003, debug=True)