import { marked } from "../lib/marked.esm.js";

export async function getSavoraResponse(message) {
  const apiUrl = "http://127.0.0.1:5000/api/v1/ai/savora";

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: "admin@mivro.org",
        message: message,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return marked.parse(data.response);
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
}

export function renderMessage(content, parent, isUser = true) {
  if (!parent || !(parent instanceof HTMLElement)) {
    throw new Error("Invalid parent element");
  }

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.classList.add(isUser ? "message-user" : "message-bot");
  messageDiv.innerHTML = content;
  parent.appendChild(messageDiv);

  parent.scrollTop = parent.scrollHeight;

  return messageDiv;
}

export async function sendHandler(inputElement, chatDiv) {
  const message = inputElement.value.trim();

  if (!message) {
    console.log("No message to send");
    return false;
  }

  inputElement.value = "";
  renderMessage(message, chatDiv);

  try {
    const response = await getSavoraResponse(message);
    renderMessage(response, chatDiv, false);
    return true;
  } catch (error) {
    console.error("Error getting Savora response:", error);
    return false;
  }
}
