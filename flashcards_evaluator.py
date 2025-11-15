from flashcards import generate_flashcards
from summarization import summarize_text_adaptive
from preprocessing import clean_text, split_sentences, chunk_text

def flashcards_evaluator(text, num_cards = 5):

    # Flashcards
    cleaned_text = clean_text(text)
    sentences = split_sentences(cleaned_text)
    chunks = chunk_text(sentences)

    # Summarization
    summary = summarize_text_adaptive(cleaned_text, chunks)

    cards = generate_flashcards(summary, num_cards)
    summary_words = summary.lower().split()

    # Number of Flashcards Generated
    total = len(cards)

    # Number of Valid Questions Generated
    valid = 0
    for question, answer in cards:
        if question.endswith('?'):
            valid += 1

    # Sets of Questions & Answers
    questions = []
    answers = []

    # Unique Flashcard Words
    unique_card_words = set()
    # Unique Overlapping Words in Both Original Text & Flashcards
    unique_overlapping = set()


    for question, answer in cards:
        questions.append(question)
        answers.append(answer)

        # Words in Flashcard
        card = f"{question} {answer}"
        card_words = card.lower().split()

        # Unique Set of Words in Flashcard
        for card_word in card_words:
            unique_card_words.add(card_word)

    # Unique Set of Overlapping Words in Both Original Text & Flashcards
    for unique_card_word in unique_card_words:
        if unique_card_word in summary_words:
            unique_overlapping.add(unique_card_word)

    # Number of Unique Questions Generated
    unique_questions = len(set(questions))
    # Number of Unique Answers Generated
    unique_answers = len(set(answers))

    # Percentage of Words in Both Original Text & Flashcards
    overlap = (len(unique_overlapping) / len(unique_card_words) * 100)

    # Number of Unique Questions & Answers Generated
    unique = min(unique_questions, unique_answers)

    print(f"Generated: {total} cards")
    print(f"Valid: {valid} / {total}")
    print(f"Unique: {unique} / {total}")
    print(f"Word Overlap: {overlap:.1f}%")

    return cards

if __name__ == "__main__":
    
    text = (

    )


    cards = flashcards_evaluator(text, 3)

    for i, (question, answer) in enumerate(cards, 1):
        print(f"\n{i}. {question}")
        print(f"   {answer}")