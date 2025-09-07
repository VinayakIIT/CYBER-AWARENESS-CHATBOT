from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
# This is useful for local development to keep your keys separate from your code.
load_dotenv()

# Flask app setup
app = Flask(__name__)
# Enable CORS for all routes and origins, allowing your frontend to connect.
CORS(app)

# OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # This check is crucial for a smooth deployment.
    # It will raise an error if the key is not found, preventing silent failures.
    raise ValueError("❌ OPENAI_API_KEY not found in environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)
print("✅ OpenAI client initialized successfully.")

# --------------------
# Routes
# --------------------

@app.route("/", methods=["GET"])
def home_route():
    """
    A simple health check route to confirm the backend is running.
    """
    return "CyberGuard Backend is live! ✅"

@app.route("/ask", methods=["POST"])
def ask_route():
    """
    Handles the main chat interaction.
    It receives a message from the frontend, sends it to OpenAI, and returns the response.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # The frontend sends a key named "message"
        question = data.get("message", "")
        
        if not question:
            return jsonify({"error": "No message provided"}), 400

        # Use OpenAI to generate an answer
        response = client.chat.completions.create(
            model="gpt-4o-mini", # A cost-effective and fast model
            messages=[
                {"role": "system", "content": "You are CyberGuard, a helpful and concise cybersecurity assistant. Explain concepts simply."},
                {"role": "user", "content": question}
            ]
        )
        
        response_text = response.choices[0].message.content
        return jsonify({"reply": response_text})

    except Exception as e:
        # Generic error handling for unexpected issues.
        print(f"Server error: {e}")
        return jsonify({"error": f"Server error: {e}"}), 500

# --------------------
# Run (for local dev)
# --------------------
if __name__ == "__main__":
    # This part is for running the app locally on your machine
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
