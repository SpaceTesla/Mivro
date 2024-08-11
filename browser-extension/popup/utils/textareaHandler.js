// utils/textareaHandler.js

export function initializeTextarea(
  textarea,
  maxRows,
  lineHeight,
  handleSend,
  chatDiv
) {
  textarea.addEventListener("input", () =>
    resizeTextarea(textarea, maxRows, lineHeight)
  );
  textarea.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault(); // Prevent adding a new line
      handleSend(textarea, chatDiv); // Send the message
    }
  });
}

function resizeTextarea(textarea, maxRows, lineHeight) {
  textarea.rows = 1; // Reset to one row to calculate the new height
  const lines = Math.ceil(textarea.scrollHeight / lineHeight);

  if (lines <= maxRows) {
    textarea.rows = lines;
    textarea.style.overflowY = "hidden"; // Hide scrollbar if within maxRows
  } else {
    textarea.rows = maxRows;
    textarea.style.overflowY = "scroll"; // Show scrollbar if maxRows exceeded
  }
}

export function resetTextarea(textarea) {
  textarea.value = ""; // Clear the textarea
  textarea.rows = 1; // Reset to one row
  textarea.style.overflowY = "hidden"; // Hide scrollbar
}
