console.log("background.js loaded");

/**
 * Fetches an SVG from a given URL and sends it as a response.
 * @param {string} url - The URL of the SVG to fetch.
 * @param {function} sendResponse - The function to call with the SVG data.
 */
function fetchSvg(url, sendResponse) {
  fetch(url)
    .then((response) => response.text())
    .then((data) => {
      sendResponse({ svg: data });
    })
    .catch((error) => {
      console.error("Error fetching SVG:", error);
      sendResponse({ error: error.toString() });
    });
}

/**
 * Fetches product information and sends it as a response.
 * @param {function} sendResponse - The function to call with the product information.
 */
function fetchProductInfo(sendResponse) {
  fetch("http://127.0.0.1:5000/api/v1/search/barcode", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: "admin@mivro.org",
      product_barcode: "8901058891430",
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
      sendResponse({ productInfo: data });
    })
    .catch((error) => {
      console.error("Fetch Failed:", error);
      sendResponse({ error: error.toString() });
    });
}

const iconPaths = {
  fetchIconM: "icons/m.svg",
  fetchIconMivro: "icons/mivro.svg",
  fetchIconShare: "icons/share.svg",
  fetchIconInfo: "icons/info.svg",
  fetchIconHeart: "icons/heart.svg",
  fetchIconClose: "icons/close.svg",
  fetchHeartFilledSvg: "icons/heart-filled.svg",
  fetchHeartSvg: "icons/heart.svg",
};

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.text in iconPaths) {
    fetchSvg(chrome.runtime.getURL(iconPaths[msg.text]), sendResponse);
    return true; // keeps the message channel open until sendResponse is called
  } else if (msg.text === "fetchProductInfo") {
    fetchProductInfo(sendResponse);
    return true; // keeps the message channel open until sendResponse is called
  } else {
    console.error(`Unknown message text: ${msg.text}`);
    sendResponse({ error: `Unknown message text: ${msg.text}` });
  }
});
