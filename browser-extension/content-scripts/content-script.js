console.log("content-script.js loaded");

// Adding the clickable div to any page
let esButton = document.createElement("div");
esButton.id = "es-btn";

let esButtonIcon = document.createElement("div");
esButtonIcon.id = "es-btn-icon";

esButton.appendChild(esButtonIcon);
document.body.appendChild(esButton);

// Adding productInfo div
let productNameString =
  document.querySelector("h1")?.innerText.split(",")[0].trim() ||
  "No Name found";

let productInfoContainer = document.createElement("div");
productInfoContainer.id = "product-info";
document.body.appendChild(productInfoContainer);

let productName = document.createElement("h1");
productName.id = "product-name";
productName.textContent = productNameString;

let closeBtn = document.createElement("div");
closeBtn.id = "close-btn";
closeBtn.textContent = " \u2715";

let productInfoContent = document.createElement("div");
productInfoContent.id = "product-info-content";

productInfoContainer.appendChild(productName);
productInfoContainer.appendChild(closeBtn);
productInfoContainer.appendChild(productInfoContent);

// Event listener for close button
closeBtn.addEventListener("click", () => {
  productInfoContainer.style.display = "none";
});

// Event listener for es button
esButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ text: "clicked_browser_action" });
  productInfoContainer.style.display = "block";

  chrome.runtime.sendMessage({ text: "get_product_info" }, (response) => {
    if (response) {
      console.log("Product Info received in response:", response);
      let productInfo = response.productInfo;
      let productInfoKeys = Object.keys(productInfo);

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
      console.error("No product info received in response:", response);
    }
  });
});
