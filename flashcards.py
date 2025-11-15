from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re

model_name = "google/flan-t5-base"
gen = pipeline("text2text-generation", model=model_name, tokenizer=model_name)

def generate_single_question(text):
    """Generate ONE question with sampling for diversity."""
    prompt = (
        "Generate ONE factual quiz question based strictly on the text. "
        "Requirements:\n"
        "- Only use facts from the text.\n"
        "- Do NOT invent new events, numbers, or assumptions.\n"
        "- Must be answerable using the text.\n"
        "- Must end with a question mark.\n\n"
        f"Text:\n{text}"
    )

    # do_sample=True enables randomness so we don't get the same question every time
    out = gen(
        prompt,
        max_new_tokens=60,
        do_sample=True,        # turn on sampling
        top_p=0.9,             # nucleus sampling for diversity
        temperature=0.7,       # slightly creative, still grounded
        num_beams=1            # beam search off; pure sampling
    )[0]["generated_text"]

    match = re.search(r"(.+?\?)", out)
    return match.group(1).strip() if match else None


def generate_answer(text, question):
    """Generate a full-sentence answer."""
    prompt = (
       "Answer the question using ONLY information explicitly stated in the text.\n"
        f"Text:\n{text}\n\n"
        f"Question: {question}"
    )
    
    out = gen(
        prompt,
        max_new_tokens=80,
        do_sample=False
    )[0]["generated_text"]

    return out.strip()


def generate_flashcards(summary_text, num_cards):
    print("\nGenerating flashcards...")

    questions = []
    attempts = 0
    MAX_ATTEMPTS = num_cards * 4   # to avoid infinite loop

    while len(questions) < num_cards and attempts < MAX_ATTEMPTS:
        attempts += 1

        q = generate_single_question(summary_text)
        if q and q not in questions:
            questions.append(q)

    flashcards = []
    for q in questions:
        a = generate_answer(summary_text, q)
        flashcards.append((q, a))

    return flashcards
    
# Dynamically determine number of cards generated based on final summary word count
def determine_num_cards(summary_text):
    wc = len(summary_text.split())

    if wc < 120:
        return 2
    elif wc < 220:
        return 3
    elif wc < 320:
        return 4
    elif wc < 450:
        return 5
    else:
        return 6


