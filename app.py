# app.py

import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from twilio_utils import download_audio_file
from transcription_utils import transcribe_audio
from sensitive_utils.detector import detect_and_encrypt_sensitive
from gemini_utils import gemini_translate
from sensitive_utils.chroma_db import load_examples

load_examples()  # Call once at startup

load_dotenv()
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    resp = MessagingResponse()
    num_media = int(request.form.get("NumMedia", 0))

    if num_media == 0:
        text = request.form.get("Body", "")
    else:
        media_url = request.form.get("MediaUrl0")
        media_type = request.form.get("MediaContentType0", "")
        if "audio" not in media_type:
            resp.message("Unsupported format. Send a voice note or text.")
            return str(resp)
        audio_bytes = download_audio_file(media_url)
        try:
            text = transcribe_audio(audio_bytes)
        except Exception as e:
            print("Transcription error:", e)
            resp.message("Error transcribing audio. Please send clear voice note.")
            return str(resp)

    secured_text = detect_and_encrypt_sensitive(text)
    translated = gemini_translate(secured_text)
    resp.message(f"Translated Output:\n\n{translated}")
    return str(resp)
