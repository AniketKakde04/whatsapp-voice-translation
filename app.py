import streamlit as st
import tempfile
from transcription_utils import transcribe_audio
from sensitive_utils.detector import detect_and_encrypt_sensitive
from gemini_utils import gemini_translate

st.set_page_config(page_title="🔐 Secure Translator", layout="centered")
st.title("🔐 Secure Voice/Text Translator")

input_mode = st.radio("Choose input mode:", ["Text", "Voice"])

if input_mode == "Text":
    user_input = st.text_area("Enter your message:")
    if st.button("Translate"):
        if user_input.strip():
            secured = detect_and_encrypt_sensitive(user_input)
            translated = gemini_translate(secured)
            st.success("Translated Output:")
            st.write(translated)

else:
    uploaded_file = st.file_uploader("Upload audio (.wav or .mp3)", type=["wav", "mp3"])
    if uploaded_file and st.button("Transcribe + Translate"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("Transcribing..."):
            transcribed = transcribe_audio(tmp_path)

        with st.spinner("Encrypting + Translating..."):
            secured = detect_and_encrypt_sensitive(transcribed)
            translated = gemini_translate(secured)

        st.success("Transcribed Text:")
        st.write(transcribed)
        st.success("Translated Output:")
        st.write(translated)
