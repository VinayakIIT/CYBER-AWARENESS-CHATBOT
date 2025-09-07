from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load API Key
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI client (new SDK)
from openai import OpenAI
client = OpenAI(api_key=api_key)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please send a message."})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=200
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"reply": "⚠️ Error processing your request."})

# Optional root route
@app.route("/", methods=["GET"])
def home():
    return "CyberGuard backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
