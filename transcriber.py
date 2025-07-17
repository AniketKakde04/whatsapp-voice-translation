import os
import tempfile
import whisper


model = whisper.load_model("tiny")

def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()

        result = model.transcribe(temp_audio.name)
        return result["text"]
