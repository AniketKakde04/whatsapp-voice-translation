from flask import Flask, request
from gemini_utils import translate_with_gemini
from twilio_utils import extract_audio_from_twilio, send_whatsapp_reply
import requests

app = Flask(__name__)

# 🔐 App B API URL
APP_B_ANALYSIS_URL = "https://YOUR-APP-B-RENDER-URL/analyze"  # Replace this with actual Render URL

def analyze_via_app_b(text: str) -> str:
    """Send text to App B's /analyze endpoint and return masked text."""
    try:
        response = requests.post(
            APP_B_ANALYSIS_URL,
            json={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("masked_text", "")
        else:
            print(f"App B returned error: {response.status_code} - {response.text}")
            return text
    except Exception as e:
        print("Error calling App B:", str(e))
        return text

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    print("✅ Received request from Twilio")
    try:
        # STEP 1: Extract audio from Twilio
        audio_bytes, from_number = extract_audio_from_twilio(request)
        if not audio_bytes:
            return "❌ No audio file found", 400

        print("🎙️ Audio received. Sending to Gemini for transcription only...")
        
        # STEP 2: Transcribe audio using Gemini (no translation yet)
        from gemini_utils import transcribe_audio_bytes
        raw_text = transcribe_audio_bytes(audio_bytes)
        print("📝 Transcribed text:", raw_text)

        if not raw_text.strip():
            send_whatsapp_reply("Sorry, I couldn't understand the audio.", from_number)
            return "✅ No speech found", 200

        # STEP 3: Analyze and mask sensitive info via App B
        encrypted_text = analyze_via_app_b(raw_text)
        print("🔐 Masked text sent to Gemini:", encrypted_text)

        # STEP 4: Translate masked text into English
        translated = translate_with_gemini(encrypted_text)
        print("🌍 Translated:", translated)

        # STEP 5: Reply to user
        send_whatsapp_reply(translated, from_number)

        return "✅ Handled successfully", 200

    except Exception as e:
        print("❌ Error:", str(e))
        return "❌ Server error", 500

if __name__ == "__main__":
    app.run(debug=True)
