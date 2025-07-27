from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

USER_SERVICE_URL = "http://user_service:5001"
NLP_SERVICE_URL = "http://nlp_service:5002"
DIALOGUE_SERVICE_URL = "http://dialogue_service:5003"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    user_response = requests.get(f"{USER_SERVICE_URL}/user/{user_id}")
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    nlp_response = requests.post(f"{NLP_SERVICE_URL}/process", json={"message": message})
    if nlp_response.status_code != 200:
        return jsonify({"error": "NLP processing failed"}), 500
    intent = nlp_response.json().get("intent")

    dialogue_response = requests.post(f"{DIALOGUE_SERVICE_URL}/respond", json={"user_id": user_id, "intent": intent, "message": message})
    if dialogue_response.status_code != 200:
        return jsonify({"error": "Dialogue processing failed"}), 500

    return jsonify({"response": dialogue_response.json().get("response")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)