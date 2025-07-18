# 🔐 Secure Voice & Text Translator

This is a local Streamlit app that:
- Accepts text or voice input (WAV/MP3)
- Detects and encrypts sensitive data (like PAN, Aadhaar, phone)
- Replaces sensitive info with labels (e.g., ***PAN***)
- Translates the cleaned text to English using Gemini API

---

## ✅ Features

- Text or voice input
- HuggingFace Whisper for transcription
- Regex + RAG-based sensitive info detection
- Encryption using Fernet
- Gemini API for translation
- Fully local except Gemini (needs internet + API key)

---
