document.getElementById('file-path').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('text-input');

  document.getElementById('loading').style.display = 'block';


  const response = await fetch('http://127.0.0.1:5500/study-prep-bot/prep.html/main', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: fileInput })
  });

  const data = await response.json();
  displayQuiz(data.summary);
});

function displayQuiz(rawData) {
  const container = document.getElementById('quiz-container');
  container.innerHTML = ''; // Clear previous content

  // Display raw JSON or text directly
  const pre = document.createElement('pre');
  pre.textContent = JSON.stringify(rawData, null, 2); // Pretty-print JSON
  container.appendChild(pre);
}
