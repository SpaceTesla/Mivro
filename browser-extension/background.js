console.log("background.js loaded");

chrome.runtime.onMessage.addListener((msg) => {
  console.log(msg.text);
});
