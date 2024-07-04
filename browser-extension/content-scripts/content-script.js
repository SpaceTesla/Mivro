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
          element.style.height = "16px";
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

chrome.runtime.sendMessage({ text: "fetchProductInfo" }, (response) => {
  if (chrome.runtime.lastError) {
    console.error("Error:", chrome.runtime.lastError.message);
  } else if (response && response.productInfo) {
    console.log("Product info received successfully:", response);
    let productInfo = response.productInfo;
    console.log(productInfo);

    let productBody = document.createElement("div");
    productBody.id = "product-body";
    document.body.appendChild(productBody);

    // Icon button setup
    let iconBtn = document.createElement("div");
    iconBtn.id = "product-btn";
    iconBtn.style.backgroundColor = productInfo.nutriscore_grade_color;

    chrome.runtime.sendMessage({ text: "fetchIconM" }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Error:", chrome.runtime.lastError.message);
      } else if (response && response.svg) {
        createAndAppendSvg(
          response.svg,
          "product-btn",
          "icon-svg",
          "white",
          () => {
            productBody.style.display = "block";
          }
        );
      } else {
        console.error("Failed to receive icon: No response received.");
      }
    });
    document.body.appendChild(iconBtn);

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

      // Heart icon with toggle click handling
      let isHeartFilled = false;

      function toggleHeartIcon() {
        let // Main product info container
          recommendation = document.createElement("div");
        recommendation.id = "product-info-container-main";
        productInfoContainer.appendChild(recommendation);

        // Product image container
        productImageContainer = document.createElement("div");
        productImageContainer.id = "product-image-container";
        recommendation.appendChild(productImageContainer);

        // Product image
        productImage = document.createElement("img");
        productImage.id = "product-image";
        selectedImages = productInfo.selected_images;
        imageUrl;

        // Iterate through the keys of selected_images object
        for (key in selectedImages) {
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
        productMainInfo = document.createElement("div");
        productMainInfo.id = "product-main-info";
        recommendation.appendChild(productMainInfo);

        // Product name
        productName = document.createElement("div");
        productName.id = "product-name";
        productName.textContent = productInfo.product_name;
        productMainInfo.appendChild(productName);

        // Brand name
        brandName = document.createElement("div");
        brandName.id = "brand-name";
        brandName.textContent = productInfo.brands;
        productMainInfo.appendChild(brandName);

        // Score container
        scoreContainer = document.createElement("div");
        scoreContainer.id = "score-container";
        productMainInfo.appendChild(scoreContainer);

        // Nutriscore color indicator
        nutriscoreScoreColor = productInfo.nutriscore_grade_color;
        nutriscoreColor = document.createElement("div");
        nutriscoreColor.id = "nutriscore-color";
        nutriscoreColor.style.backgroundColor = nutriscoreScoreColor;
        scoreContainer.appendChild(nutriscoreColor);

        // Nutriscore score container
        nutriscoreScoreContainer = document.createElement("div");
        nutriscoreScoreContainer.id = "nutriscore-score-container";
        scoreContainer.appendChild(nutriscoreScoreContainer);

        // Nutriscore score
        nutriscoreScore = document.createElement("div");
        nutriscoreScore.id = "nutriscore-score";
        nutriscoreScore.textContent = `${productInfo.nutriscore_score}/100`;
        nutriscoreScoreContainer.appendChild(nutriscoreScore);

        // Nutriscore assessment
        nutriscoreAssessment = document.createElement("div");
        nutriscoreAssessment.id = "nutriscore-assessment";
        nutriscoreAssessment.textContent = productInfo.nutriscore_assessment;
        nutriscoreScoreContainer.appendChild(nutriscoreAssessment);

        // Nutriscore grade
        nutriscoreGrade = document.createElement("div");
        nutriscoreGrade.id = "nutriscore-grade";
        nutriscoreGrade.textContent =
          productInfo.nutriscore_grade.toUpperCase();
        nutriscoreGradeColor = productInfo.nutriscore_grade_color;
        nutriscoreGrade.style.color = nutriscoreGradeColor;
        scoreContainer.appendChild(nutriscoreGrade);
        action = isHeartFilled ? "fetchHeartSvg" : "fetchHeartFilledSvg";
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
            newSvgNode.style.height = "16px";
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

      await getAndAppendIcon("share", "function-icon-div", "share-svg");
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
    let selectedImages = productInfo.selected_images;
    let imageUrl;

    // Iterate through the keys of selected_images object
    for (let key in selectedImages) {
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
    let nutriscoreScoreColor = productInfo.nutriscore_grade_color;
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

    // Nutriscore assessment
    let nutriscoreAssessment = document.createElement("div");
    nutriscoreAssessment.id = "nutriscore-assessment";
    nutriscoreAssessment.textContent = productInfo.nutriscore_assessment;
    nutriscoreScoreContainer.appendChild(nutriscoreAssessment);

    // Nutriscore grade
    let nutriscoreGrade = document.createElement("div");
    nutriscoreGrade.id = "nutriscore-grade";
    nutriscoreGrade.textContent = productInfo.nutriscore_grade.toUpperCase();
    let nutriscoreGradeColor = productInfo.nutriscore_grade_color;
    nutriscoreGrade.style.color = nutriscoreGradeColor;
    scoreContainer.appendChild(nutriscoreGrade);

    function createNutrientContainer(containerId, containerTitle, nutrients) {
      let container = document.createElement("div");
      container.id = containerId;
      container.classList.add("grade-container");
      productInfoContainer.appendChild(container);

      let title = document.createElement("div");
      title.id = `${containerId}-title`;
      title.textContent = containerTitle;
      title.classList.add("grade-title");
      container.appendChild(title);

      nutrients.forEach((nutrient) => {
        console.log(nutrient);
        let nutrientDiv = document.createElement("div");
        nutrientDiv.classList.add("nutrient");
        container.appendChild(nutrientDiv);

        let centerDiv = document.createElement("div");
        centerDiv.classList.add("nutrient-center");
        nutrientDiv.appendChild(centerDiv);

        let nutrientName = document.createElement("div");
        nutrientName.innerText = nutrient.name;
        nutrientName.classList.add("nutrient-name");
        centerDiv.appendChild(nutrientName);

        let nutrientText = document.createElement("div");
        nutrientText.innerText = nutrient.text;
        nutrientText.classList.add("nutrient-text");
        centerDiv.appendChild(nutrientText);

        let rightDiv = document.createElement("div");
        rightDiv.classList.add("nutrient-right");
        nutrientDiv.appendChild(rightDiv);

        let quantityDiv = document.createElement("div");
        quantityDiv.innerText = nutrient.quantity;
        quantityDiv.classList.add("nutrient-quantity");
        rightDiv.appendChild(quantityDiv);

        let colorDiv = document.createElement("div");
        colorDiv.style.backgroundColor = nutrient.color;
        colorDiv.classList.add("nutrient-color");
        rightDiv.appendChild(colorDiv);
      });
    }

    createNutrientContainer(
      "negatives-container",
      "Negatives",
      productInfo.nutriments.negative_nutrient
    );
    createNutrientContainer(
      "positives-container",
      "Positives",
      productInfo.nutriments.positive_nutrient
    );

    let allergiesContainer = document.createElement("div");
    allergiesContainer.id = "allergies-container";
    productInfoContainer.appendChild(allergiesContainer);

    let allergiesTitle = document.createElement("div");
    allergiesTitle.id = `allergies-title`;
    allergiesTitle.textContent = "Allergies";
    allergiesTitle.classList.add("grade-title");
    allergiesContainer.appendChild(allergiesTitle);

    productInfo.allergens_tags.forEach((allergy) => {
      let allergyDiv = document.createElement("div");
      allergyDiv.classList.add("allergy");
      allergy =
        allergy.charAt(0).toUpperCase() + allergy.substring(1, allergy.length);
      allergyDiv.innerText = allergy;
      allergiesContainer.appendChild(allergyDiv);
    });

    let additivesContainer = document.createElement("div");
    additivesContainer.id = "additives-container";
    productInfoContainer.appendChild(additivesContainer);

    let additivesTitle = document.createElement("div");
    additivesTitle.id = `additives-title`;
    additivesTitle.textContent = "Health Risks";
    additivesTitle.classList.add("grade-title");
    additivesContainer.appendChild(additivesTitle);

    let recommendationTitle = document.createElement("div");
    recommendationTitle.id = `recommendation-title`;
    recommendationTitle.textContent = "Recommendation";
    recommendationTitle.classList.add("grade-title");
    productInfoContainer.appendChild(recommendationTitle);

    // Main product info container
    recommendation = document.createElement("div");
    recommendation.id = "product-info-container-main";
    productInfoContainer.appendChild(recommendation);

    // Product image container
    productImageContainer = document.createElement("div");
    productImageContainer.id = "product-image-container";
    recommendation.appendChild(productImageContainer);

    // Product image
    productImage = document.createElement("img");
    productImage.id = "product-image";
    selectedImages = productInfo.recommeded_product.selected_images;
    imageUrl;

    // Iterate through the keys of selected_images object
    for (key in selectedImages) {
      if (selectedImages.hasOwnProperty(key)) {
        imageUrl = selectedImages[key];
        break;
      }
    }

    productImage.src = imageUrl;
    productImageContainer.appendChild(productImage);

    // Product main info container
    productMainInfo = document.createElement("div");
    productMainInfo.id = "product-main-info";
    recommendation.appendChild(productMainInfo);

    // Product name
    productName = document.createElement("div");
    productName.id = "product-name";
    productName.textContent = productInfo.recommeded_product.product_name;
    productMainInfo.appendChild(productName);

    // Brand name
    brandName = document.createElement("div");
    brandName.id = "brand-name";
    brandName.textContent = productInfo.recommeded_product.brands;
    productMainInfo.appendChild(brandName);

    // Score container
    scoreContainer = document.createElement("div");
    scoreContainer.id = "score-container";
    productMainInfo.appendChild(scoreContainer);

    // Nutriscore color indicator
    nutriscoreScoreColor =
      productInfo.recommeded_product.nutriscore_grade_color;
    nutriscoreColor = document.createElement("div");
    nutriscoreColor.id = "nutriscore-color";
    nutriscoreColor.style.backgroundColor = nutriscoreScoreColor;
    scoreContainer.appendChild(nutriscoreColor);

    // Nutriscore score container
    nutriscoreScoreContainer = document.createElement("div");
    nutriscoreScoreContainer.id = "nutriscore-score-container";
    scoreContainer.appendChild(nutriscoreScoreContainer);

    // Nutriscore score
    nutriscoreScore = document.createElement("div");
    nutriscoreScore.id = "nutriscore-score";
    nutriscoreScore.textContent = `${productInfo.recommeded_product.nutriscore_score}/100`;
    nutriscoreScoreContainer.appendChild(nutriscoreScore);

    // Nutriscore assessment
    nutriscoreAssessment = document.createElement("div");
    nutriscoreAssessment.id = "nutriscore-assessment";
    nutriscoreAssessment.textContent =
      productInfo.recommeded_product.nutriscore_assessment;
    nutriscoreScoreContainer.appendChild(nutriscoreAssessment);

    // Nutriscore grade
    nutriscoreGrade = document.createElement("div");
    nutriscoreGrade.id = "nutriscore-grade";
    nutriscoreGrade.textContent = productInfo.nutriscore_grade.toUpperCase();
    nutriscoreGradeColor =
      productInfo.recommeded_product.nutriscore_grade_color;
    nutriscoreGrade.style.color = nutriscoreGradeColor;
    scoreContainer.appendChild(nutriscoreGrade);
  } else {
    console.error("Failed to receive product info: No response received.");
  }
});
