from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend

# Load OpenAI client securely from environment variable
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment variables!")

client = OpenAI(api_key=api_key)
print("✅ OpenAI client initialized successfully")

# Route to handle chat requests
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    try:
        # Using OpenAI GPT-4 response (adjust model as needed)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are CyberGuard, a helpful cybersecurity assistant."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=250
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Error processing your request."}), 500

# Health check endpoint
@app.route("/", methods=["GET"])
def home():
    return "CyberGuard backend is running!", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


@app.route("/", methods=["GET"])
def home():
    return "CyberGuard backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

