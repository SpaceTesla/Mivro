console.log("content-script.js loaded");

// Adding the clickable div to any page
let elxrBtn = document.createElement("div");
elxrBtn.id = "elxr-btn";

let elxrBtnIcon = document.createElement("div");
elxrBtnIcon.id = "elxr-btn-icon";

elxrBtn.appendChild(elxrBtnIcon);
document.body.appendChild(elxrBtn);

// Adding productInfo div
let productNameString =
  document.querySelector("h1")?.innerText.split(",")[0].trim() ||
  "No Name found";

let productInfo = document.createElement("div");
productInfo.id = "product-info";

let productName = document.createElement("h1");
productName.id = "product-name";
productName.textContent = productNameString;

let closeBtn = document.createElement("div");
closeBtn.id = "close-btn";
closeBtn.textContent = " \u2715";

productInfo.appendChild(productName);
productInfo.appendChild(closeBtn);

document.body.appendChild(productInfo);

// No need to redeclare these variables, you can use the ones you declared earlier
elxrBtn.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "clicked_browser_action" });
  productInfo.style.display = "block";
});

closeBtn.addEventListener("click", () => {
  productInfo.style.display = "none";
});
