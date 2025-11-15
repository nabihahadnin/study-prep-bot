import time

from summarization import summarize_text_adaptive
from preprocessing import clean_text, split_sentences, chunk_text

def summarization_evaluator(original_text):
    
    # Summarization
    cleaned_text = clean_text(original_text)
    sentences = split_sentences(cleaned_text)
    chunks = chunk_text(sentences)
    summary = summarize_text_adaptive(cleaned_text, chunks)

    # Word Count of Original Text
    original_words = len(original_text.split())
    # Word Count of Summarization
    summarization_words = len(summary.split())
    
    # Sentence Count of Original Text
    original_sentences = original_text.count('.') + original_text.count('!') + original_text.count('?')
    # Sentence Count of Summarization
    summarization_sentences = summary.count('.') + summary.count('!') + summary.count('?')
    
    # Set of Words in Original Text
    original_words_set = set(original_text.lower().split())
    # Set of Words in Summarization
    summarization_words_set = set(summary.lower().split())

    # Percentage of Words in Both Original Text & Summarization
    overlap = len(original_words_set & summarization_words_set) / len(summarization_words_set) * 100
    
    print(f"Original: {original_words} words, {original_sentences} sentences")
    print(f"Summary: {summarization_words} words, {summarization_sentences} sentences")
    print(f"Word overlap: {overlap:.1f}%")

    return summary

if __name__ == "__main__":

    text = (

    )

    start_time = time.time()
    summary = summarization_evaluator(text)
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Summary : {summary}")
    print(f"Execution time: {elapsed_time:.6f} second")