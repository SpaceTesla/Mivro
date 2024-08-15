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
function fetchProductInfo(sendResponse, product) {
  fetch("http://127.0.0.1:5000/api/v1/search/database", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Mivro-Email": "test@gmail.com",
      "Mivro-Password": "test123",
    },
    body: JSON.stringify({
      product_keyword: product,
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
  fetchIconM: "assets/btn-icons/m.svg",
  fetchIconMivro: "assets/oth-icons/mivro.svg",
  fetchIconClose: "assets/btn-icons/close.svg",
  fetchIconShare: "assets/btn-icons/share.svg",
  fetchIconHeart: "assets/btn-icons/heart.svg",
  fetchHeartFilledSvg: "assets/btn-icons/heart-filled.svg",
  fetchHeartSvg: "assets/btn-icons/heart.svg",
  fetchIconInfo: "assets/btn-icons/info.svg",
  fetchIconFlag: "assets/btn-icons/flag.svg",
  fetchIconGemini: "assets/oth-icons/gemini.svg",
};

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.text in iconPaths) {
    fetchSvg(chrome.runtime.getURL(iconPaths[msg.text]), sendResponse);
    return true; // keeps the message channel open until sendResponse is called
  } else if (msg.text === "fetchProductInfo") {
    fetchProductInfo(sendResponse, msg.product);
    return true; // keeps the message channel open until sendResponse is called
  } else {
    console.error(`Unknown message text: ${msg.text}`);
    sendResponse({ error: `Unknown message text: ${msg.text}` });
  }
});
