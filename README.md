# Study Prep Bot
AI-powered tool that summarizes long documents and automatically generates flashcards to help students study more efficiently.

This project processes PDFs, DOCX files, and txt files, breaking them into chunks, summarizing them using a transformer model, and generating quiz-style flashcards using a text-to-text model. It includes a simple web interface to upload documents and receive summaries + flashcards instantly.

## Features

### Document Summarization
- Uses a transformer model (`sshleifer/distilbart-cnn-12-6`)
- Handles long documents by intelligently chunking text
- Produces concise, hierarchical summaries

### Flashcard Generation
- Automatically generates question–answer pairs from text
- Uses Flan-T5 (`google/flan-t5-base`)
- Cleaned, formatted output for studying or exporting

### Multiple File Types Supported
- PDF
- DOCX
- TXT

### Simple Web Interface
- Upload a file
- View summary + flashcards on the same page
- Lightweight front-end (HTML, CSS, JS)

## Tech Stack

- **Python 3**
- **Flask** for the web server
- **Transformers (HuggingFace)** for summarization & Q/A generation
- **PyPDF2**, **python-docx** for file parsing
- **spaCy / regex** for text cleaning
- **HTML + CSS + JavaScript** for UI

## Project Structure

```
study-prep-bot/
│
├── main.py                # Flask app entry point
├── summarization.py       # Summarization pipeline
├── flashcards.py          # Flashcard generation logic
├── preprocessing.py       # Text extraction, cleaning, chunking
│
├── templates/
│   └── prep.html          # Frontend template
│
├── static/
│   ├── prep.css
│   └── prep.js
│
├── test/                  # Sample input files
│   ├── sample-doc.docx
│   ├── sample-pdf.pdf
│   └── sample-text.txt
│
├── requirements.txt
└── README.md
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/study-prep-bot.git
cd study-prep-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3️. Run the Flask app

```bash
python main.py
```

### 4. Open in browser

```
http://127.0.0.1:5000
```

## How It Works

### **1. Preprocessing**
- Extract raw text from PDF/DOCX/TXT
- Normalize whitespace & remove artifacts
- Split text into chunks (to avoid token limits)

### **2. Summarization**
Each chunk is summarized using:
```
sshleifer/distilbart-cnn-12-6
```

If the text exceeds model limits, the system performs *hierarchical summarization*.

### **3. Flashcard Generation**
For each summarized chunk:
- Questions generated using:
```
google/flan-t5-base
```
- Answers generated using Q/A prompt  
- Output cleaned & deduplicated

## Acknowledgements

- HuggingFace Transformers
- T5 & BART research teams
- Flask
- Open-source community

