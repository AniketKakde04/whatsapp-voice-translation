import re
import nltk
from nltk.tokenize import sent_tokenize
from sensitive_utils.encryptor import encrypt_text, sensitive_data_log
from sensitive_utils.rag_faiss import LightweightRAG

nltk.download('punkt')

PATTERNS = [
    (r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', 'PAN'),
    (r'\b\d{4}\s?\d{4}\s?\d{4}\b', 'AADHAAR'),
    (r'\b[6-9]\d{9}\b', 'PHONE'),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL'),
    (r'\b\d{9,18}\b', 'ACCOUNT'),
]

rag = LightweightRAG()

def detect_and_encrypt_sensitive(text: str) -> str:
    sensitive_data_log.clear()
    sentences = sent_tokenize(text)
    new_sentences = []

    for sent in sentences:
        found = False

        for pattern, label in PATTERNS:
            match = re.search(pattern, sent)
            if match:
                sent = sent.replace(match.group(), encrypt_text(match.group(), label))
                found = True

        if not found:
            example, label, distance = rag.query(sent)
            if distance < 0.5:
                sent = encrypt_text(sent, label)

        new_sentences.append(sent)

    return " ".join(new_sentences)
