import re
import spacy
from nltk import word_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from docx import Document
import nltk

# Download NLTK resources (first time only)
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Extract text

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() for page in reader.pages])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type")
    return text

# Clean text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)              # remove extra spaces/newlines
    text = re.sub(r'\[[0-9]*\]', '', text)        # remove [1], [2], etc.
    text = re.sub(r'[^A-Za-z0-9.,;:!?\'"()\-\n ]', '', text)  # keep basic symbols
    return text.strip()

# Sentence splitting

def split_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

# Chunking 

def chunk_text(sentences, max_words=120):
    chunks = []
    current = []
    length = 0
    for sent in sentences:
        words = sent.split()
        if length + len(words) <= max_words:
            current.append(sent)
            length += len(words)
        else:
            chunks.append(" ".join(current))
            current = [sent]
            length = len(words)
    if current:
        chunks.append(" ".join(current))
    return chunks

#  Test with sample

if __name__ == "__main__":

    file_path = "test/sample-pdf.pdf"

    text = extract_text(file_path)
    print("Original length:", len(text))

    cleaned = clean_text(text)
    print("\nCleaned preview:\n", cleaned[:300])

    sentences = split_sentences(cleaned)
    print("\nNumber of sentences:", len(sentences))

    chunks = chunk_text(sentences)
    print("\nNumber of chunks:", len(chunks))
    print("\nExample chunk:\n", chunks[0])