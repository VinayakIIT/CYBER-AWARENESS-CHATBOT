from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai  # <-- NEW IMPORT

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)

# --- NEW CONFIGURATION ---

# Get the API key from environment variables
# Make sure to set this in Render!
api_key = os.getenv("GOOGLE_API_KEY") # <-- NEW KEY NAME
if not api_key:
    # This check is crucial for a smooth deployment.
    raise ValueError("❌ GOOGLE_API_KEY not found in environment variables.")

# Configure the Google AI client
genai.configure(api_key=api_key)
print("✅ Google AI (Gemini) client initialized successfully.")

# Initialize the generative model with the system prompt
# This tells the AI it's the CyberGuard assistant
system_prompt = "You are CyberGuard, a helpful and concise cybersecurity assistant. Explain concepts simply."
model = genai.GenerativeModel(
    'gemini-1.5-flash',  # Use the fast, free-tier model
    system_instruction=system_prompt
)

# --------------------
# Routes (These are the same as before!)
# --------------------

@app.route("/", methods=["GET"])
def home_route():
    """
    A simple health check route to confirm the backend is running.
    """
    return "CyberGuard Backend (Google AI Edition) is live! ✅"

@app.route("/ask", methods=["POST"])
def ask_route():
    """
    Handles the main chat interaction.
    It receives a message from the frontend, sends it to Google AI, and returns the response.
    """
    try:
        # Get JSON data from the request (This is identical to your old code)
        data = request.get_json()
        question = data.get("message", "")
        
        if not question:
            return jsonify({"error": "No message provided"}), 400

        # --- NEW API CALL ---
        # Generate the answer using the Google AI model
        response = model.generate_content(question)
        response_text = response.text
        # --- END NEW API CALL ---
        
        # Send the response back in the *exact same format* as before
        return jsonify({"reply": response_text})

    except Exception as e:
        # Generic error handling for unexpected issues.
        print(f"Server error: {e}")
        return jsonify({"error": f"Server error: {e}"}), 500

# --------------------
# Run (for local dev)
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
