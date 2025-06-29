// Cycle through preferences 0 to 3 on click
function cyclePreference(cell) {
  let current = parseInt(cell.innerText);
  if (isNaN(current)) {
    current = 0;
  }
  let newValue = (current + 1) % 4;
  if (newValue === 0) {
    cell.innerText = "X";
  } else {
    cell.innerText = newValue;
  }

  // Remove previous value classes
  cell.classList.remove("value-0", "value-1", "value-2", "value-3");

  // Add new value class
  if (newValue !== 0) {
    cell.classList.add("value-" + newValue);
  }
}

// Handle form submission
function handleFormSubmit(event) {
  event.preventDefault();

  const preferences = {};
  document.querySelectorAll(".time-slot").forEach((cell) => {
    const id = cell.getAttribute("data-id");
    const value = parseInt(cell.innerText);
    if (isNaN(value)) return;
    if (id && value !== 0) preferences[id] = value;
  });

  // Obtener el valor del checkbox
  const minDias = document.getElementById("minDiasCheckbox").checked;

  fetch("/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ preferences, min_dias: minDias }),
  })
    .then((response) => response.json())
    .then((data) => {
      const confirmation = document.getElementById("confirmation");
      confirmation.classList.remove("d-none", "alert-danger", "alert-success");
      if (data.error) {
        confirmation.classList.add("alert-danger");
        confirmation.innerHTML = `<p>Error: ${data.error}</p>`;
      } else {
        confirmation.classList.add("alert-success");
        confirmation.innerHTML = `<p>Preferencias enviadas correctamente.</p>`;
      }
    })
    .catch((error) => {
      const confirmation = document.getElementById("confirmation");
      confirmation.classList.remove("d-none", "alert-success");
      confirmation.classList.add("alert-danger");
      confirmation.innerHTML = `<p>Error: ${error.message}</p>`;
    });
}

function handleThemeUpdate() {
  const getStoredTheme = () => localStorage.getItem("theme");
  const setStoredTheme = (theme) => localStorage.setItem("theme", theme);

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) return storedTheme;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  };

  const setTheme = (theme) => {
    document.documentElement.setAttribute("data-bs-theme", theme);
  };

  // Toggle theme
  const currentTheme =
    document.documentElement.getAttribute("data-bs-theme") ||
    getPreferredTheme();
  const nextTheme = currentTheme === "dark" ? "light" : "dark";
  setStoredTheme(nextTheme);
  setTheme(nextTheme);
}
