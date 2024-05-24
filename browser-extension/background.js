console.log("background.js loaded");

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.text === "get_product_info") {
    fetch("http://127.0.0.1:5000/api/v1/search/barcode", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: "admin@mivro.org",
        product_barcode: "8901595862962",
      }),
      timeout: 15000,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to fetch data: HTTP Status ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Fetch Successful:", data);
        if (sendResponse && typeof sendResponse === "function") {
          sendResponse({ productInfo: data });
        } else {
          console.error("Failed to send response: 'sendResponse' function not found.");
        }
      })
      .catch((error) => {
        console.error("Fetch Failed:", error);
        if (sendResponse && typeof sendResponse === "function") {
          sendResponse({ error: error.toString() });
        } else {
          console.error("Failed to send response: 'sendResponse' function not found.");
        }
      });
    return true; // indicates that the response will be sent asynchronously
  }
});
