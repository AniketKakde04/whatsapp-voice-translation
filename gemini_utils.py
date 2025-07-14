import google.generativeai as genai
import os
import re
from security_utils import encrypt_text

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Holds encrypted sensitive items per request
sensitive_data_log = []

def mask_sensitive_data(text: str) -> str:
    patterns = [
        (r'\b(?:\d[ -]*?){13,16}\b', '****CARD****'),
        (r'\b\d{4,6}\b', '***PIN***'),
        (r'\b[A-Z]{4}0[A-Z0-9]{6}\b', '***IFSC***'),
        (r'\b\d{9,18}\b', '***ACCOUNT***'),
        (r'\b[6-9]\d{9}\b', '***PHONE***'),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '***EMAIL***'),
        (r'\b[\w.\-]{2,256}@[a-z]{2,10}\b', '***UPI***'),
        (r'\b\d{4}\s?\d{4}\s?\d{4}\b', '***AADHAAR***'),
        (r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', '***PAN***'),
        (r'\b[A-Z]{3}\d{7}\b', '***PASSPORT***'),
        (r'\b\d{2}[A-Z]{3}\d{4}\b', '***VEHICLE***'),
        (r'\b\d{2}/\d{2}/\d{4}\b', '***DATE***'),
        (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '***IP***'),
    ]

    def mask_and_store(match, label):
        original = match.group()
        encrypted = encrypt_text(original)
        sensitive_data_log.append((label, encrypted))
        return label

    for regex, label in patterns:
        text = re.sub(regex, lambda m: mask_and_store(m, label), text)

    return text

def transcribe_and_translate(audio_bytes: bytes) -> str:
    global sensitive_data_log
    sensitive_data_log.clear()

    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content([
        "You are an AI assistant. The user will send you a voice note in an Indian language. Do not transcribe it. Only return the English translation.",
        {
            "mime_type": "audio/mp3",
            "data": audio_bytes
        }
    ])

    translated = response.text.strip()
    secured_text = mask_sensitive_data(translated)

    if sensitive_data_log:
        return f"""📝 {secured_text}
⚠️ Please avoid sharing personal or sensitive information like card numbers, PINs, Aadhaar, etc."""
    return secured_text
