from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# ✅ Force-load .env from the same folder as app.py
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# ✅ Debug check
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(f"❌ OPENAI_API_KEY not found in {env_path}")

print("✅ API Key loaded:", api_key[:6] + "..." if api_key else "None")

# ✅ OpenAI SDK compatibility
try:
    from openai import OpenAI   # new SDK
    client = OpenAI(api_key=api_key)
    USE_NEW_SDK = True
    print("✅ Using NEW OpenAI SDK")
except ImportError:
    import openai               # old SDK
    openai.api_key = api_key
    USE_NEW_SDK = False
    print("✅ Using OLD OpenAI SDK")
