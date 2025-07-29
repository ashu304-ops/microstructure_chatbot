from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    message = data.get("message").lower()
    doc = nlp(message)

    intents = {
        "stress_query": ["stress", "force", "area", "deformation"],
        "thermodynamics_query": ["thermodynamics", "energy", "heat", "work"],
        "material_query": ["young’s modulus", "stiffness", "elasticity", "material", "young", "modulus"],
        "mechanics_query": ["free body diagram", "force", "moment", "equilibrium"],
        "fatigue_query": ["fatigue", "failure", "cyclic loading", "crack"],
        "greeting": ["hi", "hello", "hey"],
        "farewell": ["bye", "goodbye"]
    }

    intent = "unknown"
    for intent_name, keywords in intents.items():
        if any(keyword in message for keyword in keywords):
            intent = intent_name
            break

    return jsonify({"intent": intent})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)