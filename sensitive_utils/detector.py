# sensitive_utils/detector.py

import re
import nltk
from nltk.tokenize import sent_tokenize
from sensitive_utils.encryptor import encrypt_text
from sensitive_utils.rag_faiss import LightweightRAG

nltk.download("punkt")
rag = LightweightRAG()

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

        # Regex matching
        for pattern, label in PATTERNS:
            match = re.search(pattern, sent)
            if match:
                encrypted = encrypt_text(match.group())
                sent = sent.replace(match.group(), encrypted)
                found = True

        # RAG fallback
        if not found:
            example, label, distance = rag.query(sent)
            if distance < 0.5:  # Lower = more similar
                sent = encrypt_text(sent)

        new_sentences.append(sent)

    return " ".join(new_sentences)
