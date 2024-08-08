console.log("content-script.js loaded");

let iconMap = {};

function scrapeProductDetails() {
  const hostname = window.location.hostname;

  switch (hostname) {
    case "www.bigbasket.com":
      return {
        name:
          document.querySelector("h1")?.innerText.trim() ||
          "Product name not found in h1 tag.",
      };

    case "www.zeptonow.com":
      return {
        name:
          document.querySelector("h1")?.innerText.trim() ||
          "Product name not found in h1 tag.",
      };

    case "www.swiggy.com":
      return {
        name:
          document.querySelector("h1")?.innerText.trim() ||
          "Product name not found in h1 tag.",
      };

    case "www.jiomart.com":
      return {
        name:
          document.querySelector(".product-header-name")?.innerText.trim() ||
          "Product name not found in h1 tag.",
      };

    case "www.amazon.in":
      return {
        name:
          document.querySelector("#productTitle")?.innerText.trim() ||
          "Product name not found in h1 tag.",
      };

    case "www.flipkart.com":
      return {
        name:
          document.querySelector(".VU-ZEz").innerText ||
          "Product name not found in .VU-ZEz class.",
      };

    case "blinkit.com":
      return {
        name:
          document.querySelector(".tw-text-600").innerText ||
          "Product name not found in .tw-text-600 class.",
      };

    default:
      // If the hostname doesn't match any cases, return a default value
      return {
        name: "No product name found.",
      };
  }
}

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

function cleanText(input) {
  // Remove numbers and special symbols, keeping only letters and spaces
  let cleaned = input.replace(/[^a-zA-Z\s]/g, "");

  // Remove any extra spaces left after cleaning
  cleaned = cleaned.replace(/\s+/g, " ").trim();

  return cleaned;
}

// Get the product name from the page
let product_name = scrapeProductDetails().name;
console.log(":::- ", product_name);
// let productEle = product_name;
let product = cleanText(product_name).toLowerCase();
console.log(product);

chrome.runtime.sendMessage(
  { text: "fetchProductInfo", product: product },
  (response) => {
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
        await getAndAppendIcon("flag", "function-icon-div", "flag-svg");

        // Heart icon with toggle click handling
        let isHeartFilled = false;

        function toggleHeartIcon() {
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
        await getAndAppendIcon(
          "close",
          "function-icon-div",
          "close-svg",
          () => {
            productBody.style.display = "none";
          }
        );
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
      let recommendedImages = productInfo.selected_images;
      let imageUrl;

      // Iterate through the keys of selected_images object
      for (let key in recommendedImages) {
        if (recommendedImages.hasOwnProperty(key)) {
          // Get the image URL
          imageUrl = recommendedImages[key];
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

      function createNutrientContainer(
        containerId,
        containerTitle,
        nutrients,
        isIngredient = false
      ) {
        let container = document.createElement("div");
        container.id = containerId;
        container.classList.add("grade-container");
        productInfoContainer.appendChild(container);

        if (!isIngredient) {
          let title = document.createElement("div");
          title.id = `${containerId}-title`;
          title.textContent = containerTitle;
          title.classList.add("grade-title");
          container.appendChild(title);
        }

        let errorContainer = document.createElement("div");
        errorContainer.id = `${containerId}-error`;
        container.appendChild(errorContainer);

        if (nutrients.length === 0) {
          let nutrientsDiv = document.createElement("div");
          nutrientsDiv.textContent = "No data available.";
          nutrientsDiv.classList.add("error");
          errorContainer.appendChild(nutrientsDiv);
        } else {
          let nutrientCounter = 0;
          nutrients.forEach((nutrient, index) => {
            nutrientCounter++;
            console.log(nutrient);
            let nutrientDiv = document.createElement("div");
            nutrientDiv.classList.add("nutrient");

            // Initially hide nutrients after the third one
            if (index >= 3) {
              nutrientDiv.classList.add("hide-nutrient");
            }

            container.appendChild(nutrientDiv);

            let leftDiv = document.createElement("div");
            leftDiv.classList.add("nutrient-left");
            nutrientDiv.appendChild(leftDiv);

            let nutrientIcon = document.createElement("img");

            nutrientIcon.src = chrome.runtime.getURL(
              `assets/food-icons/${nutrient.icon}.png`
            );
            nutrientIcon.onerror = function () {
              nutrientIcon.src = chrome.runtime.getURL(
                "assets/food-icons/no-image.png"
              );
            };

            nutrientIcon.classList.add("nutrient-icon");
            leftDiv.appendChild(nutrientIcon);

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

          if (nutrientCounter > 3) {
            let showMoreDiv = document.createElement("div");
            showMoreDiv.classList.add("show-more");
            showMoreDiv.innerText = "Show More";
            showMoreDiv.addEventListener("click", () => {
              let nutrients = container.querySelectorAll(".nutrient");
              nutrients.forEach((nutrient, index) => {
                if (index >= 3) {
                  nutrient.classList.toggle("hide-nutrient");
                }
              });
              showMoreDiv.innerText =
                showMoreDiv.innerText === "Show More"
                  ? "Show Less"
                  : "Show More";
            });
            container.appendChild(showMoreDiv);
          }
        }
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

      let ingredientContainer = document.createElement("div");
      ingredientContainer.id = "ingredient-container";
      productInfoContainer.appendChild(ingredientContainer);

      let ingredientTitle = document.createElement("div");
      ingredientTitle.id = "ingredient-title";
      ingredientTitle.textContent = "Ingredients";
      ingredientTitle.classList.add("grade-title");
      ingredientContainer.appendChild(ingredientTitle);

      if (productInfo.ingredients.length === 0) {
        let ingredientDiv = document.createElement("div");
        ingredientDiv.textContent = "No data available.";
        ingredientDiv.classList.add("error");
        ingredientContainer.appendChild(ingredientDiv);
      } else {
        let ingredientCounter = 0;
        productInfo.ingredients.forEach((ingredient, index) => {
          ingredientCounter++;
          let ingredientDiv = document.createElement("div");
          ingredientDiv.classList.add("ingredient");

          let ingredientIconDiv = document.createElement("div");
          ingredientIconDiv.classList.add("ingredient-icon-div");
          ingredientDiv.appendChild(ingredientIconDiv);

          let ingredientIcon = document.createElement("img");
          ingredientIcon.src = chrome.runtime.getURL(
            `assets/food-icons/${ingredient.icon}.png`
          );
          ingredientIcon.onerror = function () {
            ingredientIcon.src = chrome.runtime.getURL(
              "assets/food-icons/no-image.png"
            );
          };
          ingredientIcon.classList.add("ingredient-icon");
          ingredientIconDiv.appendChild(ingredientIcon);

          let ingredientNameDiv = document.createElement("div");
          ingredientNameDiv.innerText = ingredient.name;
          ingredientDiv.appendChild(ingredientNameDiv);
          ingredientNameDiv.classList.add("ingredient-name");

          let ingredientQuantityDiv = document.createElement("div");
          ingredientQuantityDiv.innerText = ingredient.percentage;
          ingredientDiv.appendChild(ingredientQuantityDiv);
          ingredientQuantityDiv.classList.add("ingredient-quantity");

          // Initially hide ingredients after the third one
          if (index >= 3) {
            ingredientDiv.classList.add("hide-ingredient");
          }

          ingredientContainer.appendChild(ingredientDiv);
        });

        if (ingredientCounter > 3) {
          let showMoreDiv = document.createElement("div");
          showMoreDiv.classList.add("show-more");
          showMoreDiv.innerText = "Show More";
          showMoreDiv.addEventListener("click", () => {
            let ingredients =
              ingredientContainer.querySelectorAll(".ingredient");
            ingredients.forEach((ingredient, index) => {
              if (index >= 3) {
                ingredient.classList.toggle("hide-ingredient");
              }
            });
            showMoreDiv.innerText =
              showMoreDiv.innerText === "Show More" ? "Show Less" : "Show More";
          });
          ingredientContainer.appendChild(showMoreDiv);
        }
      }

      // Nova group
      let novaGroupContainer = document.createElement("div");
      novaGroupContainer.id = "nova-group-container";
      productInfoContainer.appendChild(novaGroupContainer);

      let novaGroupTitle = document.createElement("div");
      novaGroupTitle.id = "allergies-title";
      novaGroupTitle.textContent = "Nova Group";
      novaGroupTitle.classList.add("grade-title");
      novaGroupContainer.appendChild(novaGroupTitle);

      let novaGroup = document.createElement("div");
      novaGroup.id = "nova-group";
      novaGroup.classList.add("nova-group");
      novaGroupContainer.appendChild(novaGroup);

      let novaGroupNumberDiv = document.createElement("div"); // Corrected variable name
      novaGroupNumberDiv.classList.add("nova-group-number-div"); // Corrected class addition

      let novaGroupNumber = document.createElement("img");
      novaGroupNumber.src = chrome.runtime.getURL(
        `assets/food-icons/${productInfo.nova_group}.png`
      );
      novaGroupNumber.onerror = function () {
        novaGroupNumber.src = chrome.runtime.getURL(
          "assets/food-icons/no-image.png"
        );
      };
      novaGroupNumber.classList.add("nova-group-number");
      novaGroupNumberDiv.appendChild(novaGroupNumber);

      novaGroup.appendChild(novaGroupNumberDiv);

      let novaGroupText = document.createElement("div");
      novaGroupText.classList.add("nova-group-text");
      novaGroupText.textContent = productInfo.nova_group_name;
      novaGroup.appendChild(novaGroupText);

      let healthContainer = document.createElement("div");
      healthContainer.id = "additives-container";
      productInfoContainer.appendChild(healthContainer);

      let healthTitle = document.createElement("div");
      healthTitle.id = `health-title`;
      healthTitle.textContent = "Health Risks";
      healthTitle.classList.add("grade-title");
      healthContainer.appendChild(healthTitle);

      if (
        !productInfo.health_risk ||
        Object.keys(productInfo.health_risk).length === 0 ||
        productInfo.health_risk.ingredient_warnings.length === 0
      ) {
        healthDiv.textContent = "No data available.";
        healthDiv.classList.add("error");
        healthContainer.appendChild(healthDiv);
      } else {
        let healthCounter = 0;
        productInfo.health_risk.ingredient_warnings.forEach((health, index) => {
          healthCounter++;
          let healthDiv = document.createElement("div");
          healthDiv.classList.add("health");

          // Initially hide health risks after the first one
          if (index >= 1) {
            healthDiv.classList.add("hide-health");
          }

          healthDiv.innerText = health;
          healthContainer.appendChild(healthDiv);
        });

        if (healthCounter > 1) {
          let showMoreHealthDiv = document.createElement("div");
          showMoreHealthDiv.classList.add("show-more");
          showMoreHealthDiv.innerText = "Show More";
          showMoreHealthDiv.addEventListener("click", () => {
            let healthRisks = healthContainer.querySelectorAll(".health");
            healthRisks.forEach((health, index) => {
              if (index >= 1) {
                health.classList.toggle("hide-health");
              }
            });
            showMoreHealthDiv.innerText =
              showMoreHealthDiv.innerText === "Show More"
                ? "Show Less"
                : "Show More";
          });
          healthContainer.appendChild(showMoreHealthDiv);
        }
      }

      let recommendationTitle = document.createElement("div");
      recommendationTitle.id = `recommendation-title`;
      recommendationTitle.textContent = "Recommendation";
      recommendationTitle.classList.add("grade-title");
      productInfoContainer.appendChild(recommendationTitle);

      // Main product info container
      recommendation = document.createElement("div");
      recommendation.id = "product-info-container-main";
      productInfoContainer.appendChild(recommendation);

      if (productInfo.recommeded_product.error) {
        recommendation.removeAttribute("id");
        recommendation.textContent = "No data available.";
        recommendation.classList.add("error");
      } else {
        // Product image container
        productImageContainer = document.createElement("div");
        productImageContainer.id = "product-image-container";
        recommendation.appendChild(productImageContainer);

        if (!productInfo.recommeded_product.selected_images) {
          productImage = document.createElement("img");
          productImage.classList.add("no-database");
          productImage.src = chrome.runtime.getURL(
            "assets/oth-icons/no-database.png"
          );
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
        } else {
          // Product image
          productImage = document.createElement("img");
          productImage.id = "product-image";
          newRecommendedImages = productInfo.recommeded_product.selected_images;
          imageUrl;

          // Iterate through the keys of selected_images object
          for (key in newRecommendedImages) {
            if (newRecommendedImages.hasOwnProperty(key)) {
              imageUrl = newRecommendedImages[key];
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
          nutriscoreGrade.textContent =
            productInfo.recommeded_product.nutriscore_grade.toUpperCase();
          nutriscoreGradeColor =
            productInfo.recommeded_product.nutriscore_grade_color;
          nutriscoreGrade.style.color = nutriscoreGradeColor;
          scoreContainer.appendChild(nutriscoreGrade);
        }
      }
    } else {
      console.error("Failed to receive product info: No response received.");
    }
  }
);
