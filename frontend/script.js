console.log("script.js loaded");

const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const languageSelect = document.getElementById("languageSelect");

const API_URL = window.location.origin + "/chat";

function addMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.textContent = text;
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  const payload = {
    query: text,
    language: languageSelect.value,
    return_sources: false
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("HTTP " + response.status);
    }

    const data = await response.json();
    addMessage(data.answer, "bot");

  } catch (error) {
    console.error("Chat API error:", error);
    addMessage(
      "Unable to connect to the server. Please try again.",
      "bot"
    );
  }
}

userInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});
