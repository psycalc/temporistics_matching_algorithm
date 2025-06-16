const chatBox = document.getElementById('chat-box');
const input = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const voiceBtn = document.getElementById('voice-btn');
let recognition;

function appendMessage(sender, text) {
  const div = document.createElement('div');
  div.className = 'mb-2';
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(text) {
  appendMessage('You', text);
  input.value = '';
  try {
    const response = await fetch('/chat_api', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });
    const data = await response.json();
    const reply = data.reply || 'Error';
    appendMessage('Assistant', reply);
    speak(reply);
  } catch(e) {
    appendMessage('Error', 'Could not reach server');
  }
}

function speak(text) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
  }
}

sendBtn.addEventListener('click', () => {
  if (input.value.trim()) sendMessage(input.value.trim());
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && input.value.trim()) {
    e.preventDefault();
    sendMessage(input.value.trim());
  }
});

voiceBtn.addEventListener('click', () => {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert('Speech recognition not supported');
    return;
  }
  if (!recognition) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      input.value = transcript;
      sendMessage(transcript);
    };
  }
  recognition.start();
});
