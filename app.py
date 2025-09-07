from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Flask app setup
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

# Initialize OpenAI client (new SDK)
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized successfully (new SDK)")
except ImportError:
    import openai
    openai.api_key = api_key
    print("✅ OpenAI client initialized successfully (old SDK)")

# --------------------
# Routes
# --------------------

@app.route("/", methods=["GET"])
def home_route():
    return "CyberGuard Backend is live! ✅"

@app.route("/ask", methods=["POST"])
def ask_route():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Use OpenAI to generate answer
        response_text = ""
        try:
            # New SDK
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are CyberGuard, a cybersecurity assistant."},
                    {"role": "user", "content": question}
                ]
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            response_text = f"❌ Error: {str(e)}"

        return jsonify({"reply": response_text})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# --------------------
# Run (for local dev)
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

