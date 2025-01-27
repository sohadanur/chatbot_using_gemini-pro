let form = document.querySelector('form');
let promptInput = document.querySelector('input[name="prompt"]');
let output = document.querySelector('.output');

form.onsubmit = async (ev) => {
  ev.preventDefault();
  if (!promptInput.value.trim()) {
    output.textContent = 'Please enter a question.';
    return;
  }
  output.textContent = 'Thinking... Please wait.';

  try {
    let response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: promptInput.value }),
    });

    let data = await response.json();
    if (data.error) {
      output.textContent = `Error: ${data.error}`;
    } else {
      output.textContent = data.response;
    }
  } catch (e) {
    output.textContent = `Error: ${e.message}`;
  }
};
