# app.py (App A - Updated for Secure Translation)
import os
from flask import Flask, request, jsonify
from gemini_utils import transcribe_and_translate

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Receive audio bytes from Twilio
    audio_bytes = request.data
    if not audio_bytes:
        return jsonify({"error": "No audio data received"}), 400

    # Process audio: transcribe -> mask -> translate
    try:
        translated_text = transcribe_and_translate(audio_bytes)
        return jsonify({"translated_text": translated_text}), 200
    except Exception as e:
        print(f"[ERROR] Translation pipeline failed: {e}")
        return jsonify({"error": "Failed to process audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
