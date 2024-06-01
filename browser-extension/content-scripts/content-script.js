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

  parentElement.appendChild(svgElement);

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
          element.style.height = "25px";
          element.style.cursor = "pointer";
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

// Icon button setup
let iconBtn = document.createElement("div");
iconBtn.id = "product-btn";
document.body.appendChild(iconBtn);

chrome.runtime.sendMessage({ text: "fetchIconM" }, (response) => {
  if (chrome.runtime.lastError) {
    console.error("Error:", chrome.runtime.lastError.message);
  } else if (response && response.svg) {
    createAndAppendSvg(response.svg, "product-btn", "icon-svg", "green", () => {
      productBody.style.display = "block";
    });
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

  getAndAppendIcon("info", "function-icon-div", "info-svg");
  getAndAppendIcon("share", "function-icon-div", "share-svg");

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
        newSvgNode.style.height = "25px";
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

  getAndAppendIcon("heart", "function-icon-div", "heart-svg", toggleHeartIcon);

  getAndAppendIcon("close", "function-icon-div", "close-svg", () => {
    productBody.style.display = "none";
  });
})();

let productInfoContent = document.createElement("div");
productInfoContent.id = "product-info-content";
productBody.appendChild(productInfoContent);

// Product Info Container ----------------------------------------------------
let productNameString =
  document.querySelector("h1")?.innerText.split(",")[0].trim() ||
  "Product name not found.";

// Old code ----------------------------------
chrome.runtime.sendMessage({ text: "fetchProductInfo" }, (response) => {
  if (chrome.runtime.lastError) {
    console.error("Error:", chrome.runtime.lastError.message);
  } else if (response && response.productInfo) {
    console.log("Product info received successfully:", response);
    let productInfo = response.productInfo;

    // Clear previous product info
    productInfoContent.innerHTML = "";

    const keysToExtract = [
      "product_name",
      "nova_group_name",
      "nutriscore_score",
      "nutriscore_score_color",
    ];

    // Function to create and append a <p> element to a container
    function appendParagraph(container, text) {
      let paragraph = document.createElement("p");
      paragraph.textContent = text;
      container.appendChild(paragraph);
    }

    // Function to create and append an <img> element to a container
    let imgDiv = document.createElement("div");
    imgDiv.id = "product-image-div";
    function appendImage(container, src) {
      let image = document.createElement("img");
      image.src = src;
      image.classList.add("product-image");
      imgDiv.appendChild(image);
      container.appendChild(imgDiv);
    }

    // Display selected images
    for (let key in productInfo["selected_images"]) {
      appendImage(productInfoContent, productInfo["selected_images"][key]);
    }

    // Display extracted keys
    keysToExtract.forEach((key) => {
      appendParagraph(productInfoContent, `${key}: ${productInfo[key]}`);
    });

    // Display nutrient levels
    for (let key in productInfo["nutrient_levels"]) {
      appendParagraph(
        productInfoContent,
        `${key}: ${productInfo["nutrient_levels"][key]}`
      );
    }

    // Display positive nutrients
    let positiveHeader = document.createElement("h3");
    positiveHeader.textContent = "Positive Nutrients";
    productInfoContent.appendChild(positiveHeader);

    for (let nutrient of productInfo["nutriments"]["positive_nutrient"]) {
      appendParagraph(
        productInfoContent,
        `${nutrient.name}: ${nutrient.quantity}`
      );
    }

    // Display negative nutrients
    let negativeHeader = document.createElement("h3");
    negativeHeader.textContent = "Negative Nutrients";
    productInfoContent.appendChild(negativeHeader);

    for (let nutrient of productInfo["nutriments"]["negative_nutrient"]) {
      appendParagraph(
        productInfoContent,
        `${nutrient.name}: ${nutrient.quantity}`
      );
    }
  } else {
    console.error("Failed to receive product info: No response received.");
  }
});
