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


# To debug
if __name__ == "__main__":
    text = (
        "In the first quarter of the 20th century, the Treasury Department claimed that about one million "
        "Americans—1 in 10—were dependent on opium or its derivatives. That’s an outrageously high figure, "
        "and of course, it was only an estimate. As you might have guessed, many experts were deeply skeptical, "
        "believing the number was considerably lower. There were good reasons to be leery. For one thing, there "
        "were no reliable data assessing this issue, and for another, the greater of number of people addicted to "
        "opioids, the larger the Treasury Department’s Harrison Act budget. "
    )
    cards = generate_flashcards(text, 2)

    for i, (q, a) in enumerate(cards, 1):
        print(f"\n{i}. Q: {q}")
        print(f"A: {a}")
