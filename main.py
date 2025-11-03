from preprocessing import extract_text, clean_text, split_sentences, chunk_text
from summarization import summarize_text_adaptive
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def main():
    print("Study Prep AI\n")

    # File input
    file_path = input("Enter the path to your file (e.g., test/sample-pdf.pdf): ").strip()

    # Step 2: Extract and preprocess
    print("\nRunning preprocessing...")
    text = extract_text(file_path)
    cleaned_text = clean_text(text)
    sentences = split_sentences(cleaned_text)
    chunks = chunk_text(sentences)
    print(f"Preprocessing complete: {len(chunks)} chunks generated.\n")

    # Summarization
    final_summary = summarize_text_adaptive(cleaned_text, chunks)

    # Display results
    print("\nSummarization complete!\n")
    print("Final Summary:\n")
    print(final_summary)

if __name__ == "__main__":
    main()
