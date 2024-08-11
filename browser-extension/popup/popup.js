import { initializeNavigation } from "./utils/navigation.js";
import { getSavoraResponse, renderMessage, sendHandler } from "./utils/chat.js";
import { initializeTextarea, resetTextarea } from "./utils/textareaHandler.js";

const chatDiv = document.querySelector(".chat");
const sendButton = document.querySelector(".send");
const inputElement = document.querySelector(".inp");
const chatHeader = document.querySelector(".chat-header");

sendButton.addEventListener("click", () => {
  if (!chatHeader.classList.contains("hide")) {
    chatHeader.classList.add("hide");
  }
  handleSend(inputElement, chatDiv);
});
inputElement.addEventListener("keyup", (event) => {
  if (!chatHeader.classList.contains("hide")) {
    chatHeader.classList.add("hide");
  }
  if (event.key === "Enter" && !event.shiftKey) {
    handleSend(inputElement, chatDiv);
  }
});

document.addEventListener("DOMContentLoaded", async () => {
  initializeNavigation();
});

const textarea = document.querySelector(".input-container textarea");
const maxRows = 3;
const lineHeight = 20; // Line height in pixels (must match the CSS line-height)

initializeTextarea(textarea, maxRows, lineHeight, handleSend, chatDiv);

function handleSend(inputElement, chatDiv) {
  sendHandler(inputElement, chatDiv);
  resetTextarea(textarea);
}
