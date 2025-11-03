from transformers import pipeline
from preprocessing import extract_text, clean_text, split_sentences, chunk_text

# Load summarization model (DistilBART)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text_adaptive(cleaned_text, chunks):
    # Get word count
    word_count = len(cleaned_text.split())

    print(f"Total word count: {word_count}")

    # If Short text (under ~1000 words), summarize it all together
    if word_count < 1000:
        print("\nText is short — using single-pass summarization...\n")

        max_len = min(500, int(word_count * 0.4))
        min_len = max(60, int(max_len * 0.5))

        summary = summarizer(
            cleaned_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]["summary_text"]

        print(f"Final summary word count: {len(summary.split())}")
        print(f"Compression ratio: {len(summary.split())/word_count:.2%}\n")

        return summary

    # If Long text (>= 1000 words), use summarize by chunks
    else:
        print("\nText is long — using hierarchical summarization...\n")

        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk {i+1}/{len(chunks)}...")

            input_len = len(chunk.split())
            max_len = min(150, int(input_len * 0.6))
            min_len = max(20, int(max_len * 0.5))

            if min_len >= max_len:
                min_len = max(5, max_len - 5)

            try:
                summary = summarizer(
                    chunk,
                    max_length=max_len,
                    min_length=min_len,
                    do_sample=False
                )[0]["summary_text"]
                chunk_summaries.append(summary)
            except Exception as e:
                chunk_summaries.append(f"[Error summarizing chunk {i+1}: {e}]")

        # Merge chunk summaries
        merged_text = " ".join(chunk_summaries)

        # Summarize merged text for a final cohesive version
        print("\nGenerating final combined summary...\n")
        final_summary = summarizer(
            merged_text,
            max_length=300,
            min_length=100,
            do_sample=False
        )[0]["summary_text"]

        # Print stats
        print(f"Original text word count: {word_count}")
        print(f"Merged summaries word count: {len(merged_text.split())}")
        print(f"Final summary word count: {len(final_summary.split())}")
        print(f"Compression ratio: {len(final_summary.split())/word_count:.2%}\n")

        return final_summary
