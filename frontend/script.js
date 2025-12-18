const API_BASE = "http://127.0.0.1:8000";
const chatBox = document.getElementById("chat-box");
const inputEl = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const weatherCard = document.getElementById("weather-card");
const weatherText = document.getElementById("weather-text");
const mapCard = document.getElementById("map-card");
const mapFrame = document.getElementById("mapFrame");

function appendMessage(text, className = "bot-message") {
  const msg = document.createElement("div");
  msg.className = className;
  msg.innerHTML = text.replace(/\n/g, "<br>");
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function detectHindi(text) {
  return /[ऀ-ॿ]/.test(text);
}

async function sendMessage() {
  const message = inputEl.value.trim();
  if (!message) return;

  appendMessage(message, "user-message");
  inputEl.value = "";

  const loading = appendMessage("SEARCHING...", "bot-message");

  weatherCard.style.display = "none";
  mapCard.style.display = "none";

  const lang = detectHindi(message) ? "hi" : "en";

  try {
    const res = await fetch(`${API_BASE}/chat?query=${encodeURIComponent(message)}&lang=${lang}`);
    const data = await res.json();

    loading.remove();

    appendMessage(data.reply || "Could not generate a response.", "bot-message");

    if (data.weather) {
      weatherText.textContent = data.weather;
      weatherCard.style.display = "block";
    }

    if (data.map_url) {
      mapFrame.src = data.map_url;
      mapCard.style.display = "block";
    }

  } catch (err) {
    loading.remove();
    appendMessage("⚠️ Backend not responding.", "bot-message");
  }
}

inputEl.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});

sendBtn.addEventListener("click", sendMessage);

appendMessage("Hello! I'm your Tourism Assistant. Ask me about places, hotels, weather or routes. 😊", "bot-message");
