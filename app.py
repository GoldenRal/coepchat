from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from fuzzywuzzy import fuzz

app = Flask(__name__)
CORS(app)

# Load your multi-block JSON structure
with open("brochure.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    best_match = None
    best_score = 0
    best_answer = None

    for block in data:
        for idx, question in enumerate(block["questions"]):
            score = fuzz.token_sort_ratio(user_message, question.lower())
            if score > best_score:
                best_score = score
                best_match = question
                best_answer = block["answers"][idx]

    # Threshold: You can increase to 80–85 for stricter match
    if best_score >= 70:
        return jsonify({
            "reply": best_answer,
            "match": best_match,
            "confidence": best_score
        })
    else:
        return jsonify({
            "reply": "❌ Sorry, I couldn’t find the answer in the brochure.",
            "confidence": best_score
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

