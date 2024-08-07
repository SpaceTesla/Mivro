const list = document.querySelectorAll(".nav-list li");
const containers = document.querySelectorAll(".container");

list.forEach((item, index) => {
  item.addEventListener("click", function (e) {
    // Remove active class from all list items
    list.forEach((li) => li.classList.remove("active"));
    // Add active class to the clicked list item
    e.currentTarget.classList.add("active");

    // Hide all containers
    containers.forEach((container) => container.classList.add("hidden"));
    // Show the corresponding container
    containers[index].classList.remove("hidden");
  });
});
