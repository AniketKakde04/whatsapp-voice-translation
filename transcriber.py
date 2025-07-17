# transcriber.py
import whisper
import tempfile
import os

model = whisper.load_model("tiny")  # You can use "tiny", "base", "small", etc.

def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file_path = tmp_file.name

    result = model.transcribe(tmp_file_path)
    os.remove(tmp_file_path)
    return result["text"]
