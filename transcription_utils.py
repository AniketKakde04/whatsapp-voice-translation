# transcription_utils.py

import wave
import io
import json
from vosk import Model, KaldiRecognizer

# Load model once
MODEL = Model("models/vosk-model-hi")

def transcribe_audio(audio_bytes: bytes) -> str:
    wf = wave.open(io.BytesIO(audio_bytes), "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio must be WAV PCM 16-bit mono")

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
