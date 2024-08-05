export function scrapeProductDetails() {
  const hostname = window.location.hostname;

  switch (hostname) {
    case "www.bigbasket.com":
      return {
        name:
          document.querySelector("h1")?.innerText.split(",")[0].trim() ||
          "Product name not found in h1 tag.",
      };

    case "www.flipkart.com":
      return {
        name:
          document.querySelector(".VU-ZEz").innerText ||
          "Product name not found in .VU-ZEz class.",
      };

    default:
      // If the hostname doesn't match any cases, return a default value
      return {
        name: "No product name found.",
      };
  }
}
