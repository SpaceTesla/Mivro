console.log("content-script.js loaded");

/**
 * Creates and appends an SVG element to a specified parent element.
 * @param {string} svgString - The SVG string to be parsed and appended.
 * @param {string} parentId - The ID of the parent element to which the SVG will be appended.
 * @param {string} id - The ID to be assigned to the new SVG element.
 * @param {string|null} fill - Optional fill color for the SVG.
 * @param {function|null} clickHandler - Optional click handler for the SVG.
 * @returns {Element} The appended SVG element.
 */
function createAndAppendSvg(
  svgString,
  parentId,
  id,
  fill = null,
  clickHandler = null
) {
  let parentElement = document.getElementById(parentId);
  let parser = new DOMParser();
  let svgElement = parser.parseFromString(
    svgString,
    "image/svg+xml"
  ).documentElement;
  svgElement.id = id;

  if (fill) {
    for (let child of svgElement.children) {
      child.setAttribute("fill", fill);
    }
  }
  let iconDiv = document.createElement("div");
  iconDiv.id = "icon-div";
  iconDiv.appendChild(svgElement);
  parentElement.appendChild(iconDiv);

  if (clickHandler) {
    svgElement.addEventListener("click", clickHandler);
  }

  return svgElement;
}

/**
 * Requests and appends an icon SVG to a specified parent element.
 * @param {string} iconName - The name of the icon to be fetched.
 * @param {string} parentId - The ID of the parent element to which the icon will be appended.
 * @param {string} id - The ID to be assigned to the new SVG element.
 * @param {function|null} callback - Optional click handler for the SVG.
 * @returns {Promise} A promise that resolves when the icon is appended.
 */
function getAndAppendIcon(iconName, parentId, id, callback) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(
      { text: `fetchIcon${capitalize(iconName)}` },
      (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error:", chrome.runtime.lastError.message);
          reject(chrome.runtime.lastError);
        } else if (response && response.svg) {
          let element = createAndAppendSvg(
            response.svg,
            parentId,
            id,
            null,
            callback
          );
          element.style.height = "20px";
          element.style.cursor = "pointer";
          element.classList.add("icon-svg");
          resolve();
        } else {
          console.error(`${capitalize(iconName)} Icon not received`);
          reject(new Error(`${iconName} Icon not received`));
        }
      }
    );
  });
}

/**
 * Capitalizes the first letter of a string.
 * @param {string} str - The string to be capitalized.
 * @returns {string} The capitalized string.
 */
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

let productInfo = localStorage.getItem("productInfo");

if (productInfo) {
  // Parse and use the cached product info
  productInfo = JSON.parse(productInfo);
  console.log("Product info retrieved from cache:", productInfo);
} else {
  // Fetch product info if not cached
  chrome.runtime.sendMessage({ text: "fetchProductInfo" }, (response) => {
    if (chrome.runtime.lastError) {
      console.error("Error:", chrome.runtime.lastError.message);
    } else if (response && response.productInfo) {
      console.log("Product info received successfully:", response);
      let productInfo = response.productInfo;

      // Store the product info in localStorage
      localStorage.setItem("productInfo", JSON.stringify(productInfo));
    } else {
      console.error("Failed to receive product info: No response received.");
    }
  });
}

let nutriscoreScoreColor = productInfo.nutriscore_score_color;

// Icon button setup
let iconBtn = document.createElement("div");
iconBtn.id = "product-btn";
document.body.appendChild(iconBtn);

chrome.runtime.sendMessage({ text: "fetchIconM" }, (response) => {
  if (chrome.runtime.lastError) {
    console.error("Error:", chrome.runtime.lastError.message);
  } else if (response && response.svg) {
    createAndAppendSvg(
      response.svg,
      "product-btn",
      "icon-svg",
      nutriscoreScoreColor,
      () => {
        productBody.style.display = "block";
      }
    );
  } else {
    console.error("Failed to receive icon: No response received.");
  }
});

let productBody = document.createElement("div");
productBody.id = "product-body";
document.body.appendChild(productBody);

// Navbar setup
let productNav = document.createElement("div");
productNav.id = "product-nav";
productBody.appendChild(productNav);

(async () => {
  await getAndAppendIcon("mivro", "product-nav", "mivro-svg");

  let functionIconDiv = document.createElement("div");
  functionIconDiv.id = "function-icon-div";
  productNav.appendChild(functionIconDiv);

  await getAndAppendIcon("info", "function-icon-div", "info-svg");
  await getAndAppendIcon("share", "function-icon-div", "share-svg");

  // Heart icon with toggle click handling
  let isHeartFilled = false;

  function toggleHeartIcon() {
    const action = isHeartFilled ? "fetchHeartSvg" : "fetchHeartFilledSvg";
    chrome.runtime.sendMessage({ text: action }, function (response) {
      if (chrome.runtime.lastError) {
        console.error("Error:", chrome.runtime.lastError.message);
        return;
      }
      if (response && response.svg) {
        let parser = new DOMParser();
        let newSvgNode = parser.parseFromString(
          response.svg,
          "image/svg+xml"
        ).documentElement;
        newSvgNode.style.height = "20px";
        newSvgNode.style.cursor = "pointer";
        newSvgNode.id = "heart-svg"; // Ensure the new SVG has the correct ID

        let heartIcon = document.getElementById("heart-svg");
        heartIcon.replaceWith(newSvgNode);

        // Add the click event to the new heart icon
        newSvgNode.addEventListener("click", toggleHeartIcon);

        // Toggle the state
        isHeartFilled = !isHeartFilled;
      } else {
        console.error("Failed to receive SVG: No response received.");
      }
    });
  }

  await getAndAppendIcon(
    "heart",
    "function-icon-div",
    "heart-svg",
    toggleHeartIcon
  );
  await getAndAppendIcon("close", "function-icon-div", "close-svg", () => {
    productBody.style.display = "none";
  });
})();

// Product info container setup
let productInfoContainer = document.createElement("div");
productInfoContainer.id = "product-info-container";
productBody.appendChild(productInfoContainer);

// Main product info container
let productInfoContainerMain = document.createElement("div");
productInfoContainerMain.id = "product-info-container-main";
productInfoContainer.appendChild(productInfoContainerMain);

// Product image container
let productImageContainer = document.createElement("div");
productImageContainer.id = "product-image-container";
productInfoContainerMain.appendChild(productImageContainer);

// Product image
let productImage = document.createElement("img");
productImage.id = "product-image";
const selectedImages = productInfo.selected_images;
let imageUrl;

// Iterate through the keys of selected_images object
for (const key in selectedImages) {
  if (selectedImages.hasOwnProperty(key)) {
    // Get the image URL
    imageUrl = selectedImages[key];
    // Break the loop as we only need the first image URL
    break;
  }
}

productImage.src = imageUrl;
productImageContainer.appendChild(productImage);

// Product main info container
let productMainInfo = document.createElement("div");
productMainInfo.id = "product-main-info";
productInfoContainerMain.appendChild(productMainInfo);

// Product name
let productName = document.createElement("div");
productName.id = "product-name";
productName.textContent = productInfo.product_name;
productMainInfo.appendChild(productName);

// Brand name
let brandName = document.createElement("div");
brandName.id = "brand-name";
brandName.textContent = productInfo.brands;
productMainInfo.appendChild(brandName);

// Score container
let scoreContainer = document.createElement("div");
scoreContainer.id = "score-container";
productMainInfo.appendChild(scoreContainer);

// Nutriscore color indicator
let nutriscoreColor = document.createElement("div");
nutriscoreColor.id = "nutriscore-color";
nutriscoreColor.style.backgroundColor = nutriscoreScoreColor;
scoreContainer.appendChild(nutriscoreColor);

// Nutriscore score container
let nutriscoreScoreContainer = document.createElement("div");
nutriscoreScoreContainer.id = "nutriscore-score-container";
scoreContainer.appendChild(nutriscoreScoreContainer);

// Nutriscore score
let nutriscoreScore = document.createElement("div");
nutriscoreScore.id = "nutriscore-score";
nutriscoreScore.textContent = `${productInfo.nutriscore_score}/100`;
nutriscoreScoreContainer.appendChild(nutriscoreScore);

// Nutriscore comment
let nutriscoreComment = document.createElement("div");
nutriscoreComment.id = "nutriscore-comment";
nutriscoreComment.textContent = "Bad"; // You might want to update this dynamically based on the score
nutriscoreScoreContainer.appendChild(nutriscoreComment);
