import os
import tempfile
import whisper
import ffmpeg_static

# Add ffmpeg-static to PATH so Whisper can use it
os.environ["PATH"] = ffmpeg_static.add_paths(os.environ["PATH"])

model = whisper.load_model("tiny")

def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()

        result = model.transcribe(temp_audio.name)
        return result["text"]
