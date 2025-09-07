# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Flask app
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

# OpenAI client
try:
    from openai import OpenAI  # New SDK
    client = OpenAI(api_key=api_key)
    print("✅ Using NEW OpenAI SDK")
except ImportError:
    import openai             # Old SDK fallback
    openai.api_key = api_key
    print("✅ Using OLD OpenAI SDK")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Please provide a message."})

    # Generate response using OpenAI
    try:
        if 'client' in globals():
            # New SDK
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
                temperature=0.7,
            )
            reply = response.choices[0].message.content
        else:
            # Old SDK
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
                temperature=0.7,
            )
            reply = response.choices[0].message['content']
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
