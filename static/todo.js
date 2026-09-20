document.querySelectorAll(".todo-checkbox").forEach(function (checkbox) {
  checkbox.addEventListener("change", function () {
    var row = checkbox.closest(".todo-row");
    var id = row.dataset.id;
    var errorEl = row.querySelector(".todo-error");
    var newState = checkbox.checked;

    errorEl.textContent = "";

    fetch("/todos/" + id, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: newState }),
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("request failed");
        }
        row.classList.toggle("completed", newState);
      })
      .catch(function () {
        checkbox.checked = !newState;
        row.classList.toggle("completed", !newState);
        errorEl.textContent = "Failed to save. Please try again.";
      });
  });
});
