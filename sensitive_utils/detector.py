# sensitive_utils/detector.py

from sensitive_utils.encryptor import encrypt_text
from sensitive_utils.chroma_db import query_similar
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from sensitive_utils.chroma_db import  add_example

# Still use regex patterns for known matches
PATTERNS = [
    (r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', 'PAN'),
    (r'\b\d{4}\s?\d{4}\s?\d{4}\b', 'AADHAAR'),
    (r'\b[6-9]\d{9}\b', 'PHONE'),
]

def detect_and_encrypt_sensitive(text: str) -> str:
    sentences = sent_tokenize(text)
    new_sentences = []

    for sent in sentences:
        found = False
        # Regex check
        for pattern, label in PATTERNS:
            match = re.search(pattern, sent)
            if match:
                encrypted = encrypt_text(match.group())
                sent = sent.replace(match.group(), encrypted)
                found = True
        # RAG fallback
        if not found:
            docs, metas = query_similar(sent)
            if metas and len(metas) > 0:
                encrypted = encrypt_text(sent)
                sent = encrypted
        new_sentences.append(sent)

    return " ".join(new_sentences)

def detect_and_encrypt_sensitive(text: str) -> str:
    sentences = sent_tokenize(text)
    new_sentences = []

    for sent in sentences:
        found = False
        # Regex check
        for pattern, label in PATTERNS:
            match = re.search(pattern, sent)
            if match:
                original = match.group()
                encrypted = encrypt_text(original)
                sent = sent.replace(original, encrypted)
                found = True
                # Add to Chroma for future detection
                add_example(sent, label)

        # RAG fallback
        if not found:
            docs, metas = query_similar(sent)
            if metas and len(metas) > 0:
                similarity_label = metas[0]["label"]
                # If similar to other sensitive examples, encrypt entire sentence
                encrypted = encrypt_text(sent)
                sent = encrypted
                add_example(sent, similarity_label)
            else:
                # Optional: if confident it's sensitive, still log it
                pass

        new_sentences.append(sent)

    return " ".join(new_sentences)