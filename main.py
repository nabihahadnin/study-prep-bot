from preprocessing import extract_text, clean_text, split_sentences, chunk_text
from summarization import summarize_text_adaptive
from flashcards import generate_flashcards  
import nltk


from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

@app.route('/')
def home():
    return render_template('prep.html')

@app.route('/main', methods=['POST'])
def main():
        
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    generate_type = request.form.get('type', 'summary')
    file = request.files['file']
    file_path = file.filename
    file.save(file_path)

        
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    print("Study Prep AI\n")

    # Preprocessing
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
        
    response_data = {}

    if generate_type in ['summary', 'both']:
        response_data['summary'] = final_summary

    if generate_type in ['quiz', 'both']:
        flashcards = generate_flashcards(final_summary, num_cards=5)
        flashcards_data = [{"question": q, "answer": a} for q, a in flashcards]
        response_data['flashcards'] = flashcards_data
        
        print("\nFLASHCARDS:\n")
        for i, (q, a) in enumerate(flashcards, 1):
            print(f"{i}. Q: {q}")
            print(f"   A: {a}\n")

    try:
        os.remove(file_path)
    except:
        pass

    return jsonify(response_data)


    # Generate flashcards
    flashcards = generate_flashcards(final_summary, num_cards=5)

    print("\nFLASHCARDS:\n")
    for i, (q, a) in enumerate(flashcards, 2):
        print(f"{i}. Q: {q}")
        print(f"   A: {a}\n")

if __name__ == "__main__":
    app.run(debug=True)