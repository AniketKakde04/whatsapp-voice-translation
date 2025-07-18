import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_translate(text: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(f"Translate this to English:\n{text}")
    return response.text.strip()
