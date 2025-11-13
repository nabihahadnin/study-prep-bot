from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re

model_name = "google/flan-t5-base"
gen = pipeline("text2text-generation", model=model_name, tokenizer=model_name)


def generate_single_question(text):
    """Generate ONE question safely."""
    prompt = (
        "Generate ONE question ending with a question mark. "
        "The question must be based ONLY on this text:\n\n"
        f"{text}"
    )

    out = gen(prompt, max_new_tokens=60, do_sample=False)[0]["generated_text"]

    match = re.search(r"(.+?\?)", out)
    return match.group(1).strip() if match else None


def generate_answer(text, question):
    """Generate a full-sentence answer."""
    prompt = (
        "Answer the question based ONLY on this text.\n\n"
        f"Text: {text}\n\n"
        f"Question: {question}"
    )

    out = gen(prompt, max_new_tokens=80, do_sample=False)[0]["generated_text"]
    return out.strip()


def generate_flashcards(summary_text, num_cards):
    print("\nGenerating flashcards...")

    questions = []
    attempts = 0
    MAX_ATTEMPTS = num_cards * 4

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


# Debug
if __name__ == "__main__":
    text = "In the first quarter of the 20th century, the Treasury Department claimed that about one million Americans 1 in 10 were dependent on opium or its derivatives . The greater of number of people addicted to opioids, the larger the Treasury Departments Harrison Act budget . The Harrison Act stated that an unregistered person could purchase and possess any of the taxed drugs if they had been prescribed or administered by a physician in the course of his professional practice and for legitimate medical purposes .Until the 1920s, most users continued to receive opioids through their private physicians . "
    cards = generate_flashcards(text, 5)

    for i, (q, a) in enumerate(cards, 1):
        print(f"\n{i}. Q: {q}")
        print(f"A: {a}")
