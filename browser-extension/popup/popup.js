const list = document.querySelectorAll(".nav-list li");
const nav = document.querySelector(".navigation");

list.forEach((item) => {
  item.addEventListener("click", function (e) {
    list.forEach((li) => li.classList.remove("active"));
    e.currentTarget.classList.add("active");
  });
});
