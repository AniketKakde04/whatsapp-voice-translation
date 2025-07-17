# transcription_utils.py

import os
import wave
import io
import json
import requests
import zipfile
from vosk import Model, KaldiRecognizer

MODEL_PATH = "models/vosk-model-hi"

def download_vosk_model():
    if not os.path.exists(MODEL_PATH):
        print("📦 Downloading Vosk model...")
        os.makedirs("models", exist_ok=True)
        url = "https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip"
        zip_path = "models/model.zip"
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("models/")
        os.rename("models/vosk-model-small-hi-0.22", MODEL_PATH)
        os.remove(zip_path)
        print("✅ Vosk model downloaded.")

# Ensure model exists before loading
download_vosk_model()
MODEL = Model(MODEL_PATH)

def transcribe_audio(audio_bytes: bytes) -> str:
    wf = wave.open(io.BytesIO(audio_bytes), "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio must be WAV format (PCM 16-bit mono)")

    rec = KaldiRecognizer(MODEL, wf.getframerate())
    rec.SetWords(True)

    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result += res.get("text", "") + " "

    res = json.loads(rec.FinalResult())
    result += res.get("text", "")
    return result.strip()
