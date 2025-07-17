# gemini_utils.py (App A - Clean Version)
import os
import requests
import google.generativeai as genai
from transcriber import transcribe_audio

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# URL for App B (Sensitive Info Analyzer)
APP_B_URL = "https://your-app-b-url.onrender.com/analyze"  # <-- Update this

def mask_sensitive_data_via_app_b(text: str) -> str:
    try:
        response = requests.post(APP_B_URL, json={"text": text})
        response.raise_for_status()
        return response.json().get("masked_text", text)
    except Exception as e:
        print(f"[ERROR] App B masking failed: {e}")
        return text  # fallback to unmasked

def transcribe_and_translate(audio_bytes: bytes) -> str:
    # Step 1: Transcribe
    transcript = transcribe_audio(audio_bytes)
    print(f"📝 Transcription:\n{transcript}")

    # Step 2: Mask Sensitive Info via App B
    masked_text = mask_sensitive_data_via_app_b(transcript)
    print(f"🔐 Masked Text:\n{masked_text}")

    # Step 3: Translate using Gemini
    try:
        prompt = f"Translate this to English:\n{masked_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini translation failed: {e}")
        return transcript  # fallback to original
