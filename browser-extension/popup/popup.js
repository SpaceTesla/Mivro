import { initializeNavigation } from "./utils/navigation.js";
import { getSavoraResponse, renderMessage, sendHandler } from "./utils/chat.js";
import { initializeTextarea, resetTextarea } from "./utils/textareaHandler.js";

const chatDiv = document.querySelector(".chat");
const sendButton = document.querySelector(".send");
const inputElement = document.querySelector(".inp");
const chatHeader = document.querySelector(".chat-header");

sendButton.addEventListener("click", async () => {
  let isHandeled = await handleSend(inputElement, chatDiv);
  console.log("isHandeled:", isHandeled);
  if (isHandeled && !chatHeader.classList.contains("hide")) {
    chatHeader.classList.add("hide");
  }
});
inputElement.addEventListener("keyup", (event) => {
  let isHandeled = false;
  if (event.key === "Enter" && !event.shiftKey) {
    isHandeled = handleSend(inputElement, chatDiv);
  }
  if (isHandeled && !chatHeader.classList.contains("hide")) {
    chatHeader.classList.add("hide");
  }
});

document.addEventListener("DOMContentLoaded", async () => {
  initializeNavigation();
});

const textarea = document.querySelector(".input-container textarea");
const maxRows = 3;
const lineHeight = 20; // Line height in pixels (must match the CSS line-height)

initializeTextarea(textarea, maxRows, lineHeight, handleSend, chatDiv);

async function handleSend(inputElement, chatDiv) {
  let condition = await sendHandler(inputElement, chatDiv);
  console.log("sendHandler:", condition);
  resetTextarea(textarea);
  if (condition) {
    return true;
  } else {
    return false;
  }
}
