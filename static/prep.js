document.getElementById('summary-btn').addEventListener('click', () => handleSubmit('summary'))
document.getElementById('flashcards-btn').addEventListener('click', () => handleSubmit('flashcards'))
document.getElementById('both-btn').addEventListener('click', () => handleSubmit('both'))

async function handleSubmit(type) {
 
  const fileInput = document.getElementById('file-input');
  const file = fileInput.files[0];
  if (!file) return;

  document.getElementById('loading').style.display = 'block';

  const formData = new FormData();
  formData.append('file', file);
  formData.append('type', type);


  const response = await fetch('/main', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  document.getElementById('loading').style.display = 'none'
  document.getElementById('quiz-container').innerHTML = '';
  
  if (data.summary) {
    displaySummary(data.summary);
  }

  if (data.flashcards) {
    displayFlashcards(data.flashcards);
  }

}

function displaySummary(summary) {
  const container = document.getElementById('quiz-container');
  container.innerHTML = '<h2>Summary:</h2><p style="white-space: pre-wrap; word-wrap: break-word;">' + summary + '</p>';
}

function displayFlashcards(flashcards) {
  const container = document.getElementById('quiz-container');
  
  let html = '<h2 style="margin-top: 40px;">Flashcards:</h2>';
  html += '<div id="flashcard-display"></div>';
  html += '<div class="flashcard-controls">';
  html += '<button id="prev-btn">← Previous</button>';
  html += '<button id="flip-btn">Flip Card</button>';
  html += '<button id="next-btn">Next →</button>';
  html += '</div>';
  html += '<p class="flashcard-counter"><span id="current-card">1</span> / <span id="total-cards">' + flashcards.length + '</span></p>';
  
  container.innerHTML += html;
  
  initFlashcards(flashcards);
}

let currentCard = 0;
let cards = [];
let showingAnswer = false;

function initFlashcards(flashcards) {
  cards = flashcards;
  showCard(0);
  
  document.getElementById('flip-btn').onclick = () => {
    showingAnswer = !showingAnswer;
    showCard(currentCard);
  };
  
  document.getElementById('next-btn').onclick = () => {
    if (currentCard < cards.length - 1) {
      currentCard++;
      showingAnswer = false;
      showCard(currentCard);
    }
  };
  
  document.getElementById('prev-btn').onclick = () => {
    if (currentCard > 0) {
      currentCard--;
      showingAnswer = false;
      showCard(currentCard);
    }
  };
}

function showCard(index) {
  const card = cards[index];
  const display = document.getElementById('flashcard-display');
  const text = showingAnswer ? card.answer : card.question;
  const label = showingAnswer ? 'Answer:' : 'Question:';
  
  display.innerHTML = '<div class="flashcard"><strong>' + label + '</strong><p>' + text + '</p></div>';
  document.getElementById('current-card').textContent = index + 1;
}
