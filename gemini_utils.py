import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

def translate_text(text):
    prompt = f"""Translate this sentence to English (if needed) and fix grammar and sentence structure:
    
    Sentence: {text}
    
    Only return the final cleaned English sentence."""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Translation error:", e)
        return text

def forward_to_analyzer(text):
    try:
        response = requests.post(
            "http://localhost:8000/analyze",  # Update this URL if you deploy App B later
            json={"text": text},
            timeout=10
        )
        return response.json()
    except Exception as e:
        print("❌ Analyzer service error:", e)
        return {"secured_text": text, "log": []}

def transcribe_and_translate(transcript):
    translated = translate_text(transcript)
    result = forward_to_analyzer(translated)
    secured_text = result["secured_text"]
    sensitive_data_log = result["log"]

    if sensitive_data_log:
        return f"""📝 {secured_text}
⚠️ Sensitive info was detected and encrypted securely. Avoid sharing such data in the future."""
    else:
        return f"📝 {secured_text}"
