from transformers import pipeline, AutoTokenizer
from preprocessing import extract_text, clean_text, split_sentences, chunk_text
from nltk.tokenize import sent_tokenize
import re

# Load summarizer + tokenizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

# Post-Summarization cleaning + smoothing helpers
def clean_summary_text(text):
    # Fix punctuation and double spaces
    text = re.sub(r"\s+\.", ".", text)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def smooth_sentences(text):
    # Remove tiny fragments and ensure clean sentence boundaries
    sents = sent_tokenize(text)
    cleaned = []

    for s in sents:
        s = s.strip()

        # Capitalize first letter if missing
        if s and not s[0].isupper():
            s = s[0].upper() + s[1:]

        cleaned.append(s)

    merged = " ".join(cleaned)

    # Ensure ending punctuation
    if merged and not merged.endswith((".", "!", "?")):
        merged += "."

    return merged

# Summarization using tokens to follow the boundary of distilBART's model
def summarize_text_adaptive(cleaned_text, chunks):
    """
    Token-based switch:
    - If input tokens <= 900 → single-pass summarization
    - If >900 → hierarchical summarization
    
    This is to ensure no broken-ending filtering and preserve more ore content
    """

    num_tokens = len(tokenizer.encode(cleaned_text))
    print(f"Total tokens: {num_tokens}")

    MAX_TOKENS = 900   # safe threshold for DistilBART (<1024)

    # CASE 1 — SINGLE-PASS (SAFE LENGTH)
    if num_tokens <= MAX_TOKENS:
        print("Single-pass summarization...")

        word_count = len(cleaned_text.split())
        target_words = int(word_count * 0.25)   # ~25% target
        target_tokens = int(target_words * 1.3)

        max_len = min(512, target_tokens)
        min_len = max(40, int(max_len * 0.5))

        result = summarizer(
            cleaned_text,
            max_length=max_len,
            min_length=min_len,
            no_repeat_ngram_size=3,
            do_sample=False
        )

        summary = result[0]["summary_text"]

        summary = clean_summary_text(summary)
        summary = smooth_sentences(summary)

        print(f"Summary words: {len(summary.split())}")
        return summary

    # CASE 2 — HIERARCHICAL SUMMARIZATION
    print("Hierarchical summarization (token limit exceeded)...")

    chunk_summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}/{len(chunks)}...")

        # If chunk is too small, skip summarization
        if len(chunk.split()) < 40:
            cleaned = clean_summary_text(chunk)
            cleaned = smooth_sentences(cleaned)
            if cleaned:
                chunk_summaries.append(cleaned)
            continue

        # Target ~30% of each chunk
        chunk_wc = len(chunk.split())
        chunk_target_words = int(chunk_wc * 0.30)
        chunk_target_tokens = int(chunk_target_words * 1.3)

        max_len = min(256, chunk_target_tokens)
        min_len = max(30, int(max_len * 0.5))

        result = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            no_repeat_ngram_size=3,
            do_sample=False
        )

        cleaned = result[0]["summary_text"]
        cleaned = clean_summary_text(cleaned)
        cleaned = smooth_sentences(cleaned)

        if cleaned:
            chunk_summaries.append(cleaned)

    # Merge chunks
    merged = " ".join(s for s in chunk_summaries)

    merged = clean_summary_text(merged)
    merged = smooth_sentences(merged)

    print(f"Final merged summary words: {len(merged.split())}")
    return merged
