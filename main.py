from preprocessing import extract_text, clean_text, split_sentences, chunk_text
from summarization import summarize_text_adaptive
from flashcards import generate_flashcards  
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def main():
    print("Study Prep AI\n")

    # Get file path
    file_path = input("Enter the path to your file (e.g., test/sample-pdf.pdf): ").strip()

    # Preprocessing
    print("\nRunning preprocessing...")
    text = extract_text(file_path)
    cleaned_text = clean_text(text)
    sentences = split_sentences(cleaned_text)
    chunks = chunk_text(sentences)
    print(f"Preprocessing complete: {len(chunks)} chunks generated.\n")

    # Summarization
    final_summary = summarize_text_adaptive(cleaned_text, chunks)
    print("\nFINAL SUMMARY:\n")
    print(final_summary)

    # Generate flashcards
    flashcards = generate_flashcards(final_summary, num_cards=5)

    print("\nFLASHCARDS:\n")
    for i, (q, a) in enumerate(flashcards, 2):
        print(f"{i}. Q: {q}")
        print(f"   A: {a}\n")

if __name__ == "__main__":
    main()
