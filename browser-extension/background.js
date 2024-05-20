console.log("background.js loaded");

// chrome.runtime.onMessage.addListener((msg) => {
//   console.log(msg.text);
// });
console.log("background.js loaded");

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.text === "get_product_info") {
    fetch("http://127.0.0.1:5000/api/v1/search/barcode", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_barcode: "8901595862962",
      }),
      timeout: 15000,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Success:", data);
        if (sendResponse && typeof sendResponse === "function") {
          sendResponse({ productInfo: data });
        } else {
          console.error("sendResponse is not available.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        if (sendResponse && typeof sendResponse === "function") {
          sendResponse({ error: error.toString() });
        } else {
          console.error("sendResponse is not available.");
        }
      });
    return true; // indicates that the response will be sent asynchronously
  }
});
