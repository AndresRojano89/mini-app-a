const passwordOutput = document.querySelector("#password-output");
const generateButton = document.querySelector("#generate-button");
const copyButton = document.querySelector("#copy-button");
const lengthSlider = document.querySelector("#length-slider");
const lengthValue = document.querySelector("#length-value");
const strengthMeter = document.querySelector(".strength-meter");
const strengthLabel = document.querySelector("#strength-label");
const entropyLabel = document.querySelector("#entropy-label");
const errorMessage = document.querySelector("#error-message");

function updateSlider() {
  const min = Number(lengthSlider.min);
  const max = Number(lengthSlider.max);
  const value = Number(lengthSlider.value);
  const percentage = ((value - min) / (max - min)) * 100;
  lengthSlider.style.background = `linear-gradient(to right, #5e9668 ${percentage}%, #e8ece7 ${percentage}%)`;
  lengthValue.value = value;
  lengthValue.textContent = value;
}

async function generatePassword() {
  generateButton.disabled = true;
  generateButton.setAttribute("aria-busy", "true");
  errorMessage.hidden = true;

  const options = Object.fromEntries(
    [...document.querySelectorAll('.option-row input[type="checkbox"]')].map((input) => [
      input.name,
      input.checked,
    ]),
  );
  options.length = Number(lengthSlider.value);
  options.exclude_similar = document.querySelector("#exclude-similar").checked;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options),
      cache: "no-store",
    });
    const result = await response.json();
    if (!response.ok) {
      const detail = typeof result.detail === "string" ? result.detail : null;
      throw new Error(detail || "No se pudo generar la contraseña.");
    }

    passwordOutput.textContent = result.password;
    passwordOutput.classList.remove("is-empty");
    strengthLabel.textContent = result.strength;
    entropyLabel.textContent = `${result.entropy} bits`;
    const levels = { Básica: 1, Buena: 2, Fuerte: 3, Excelente: 4 };
    strengthMeter.dataset.level = levels[result.strength] || 0;
    copyButton.disabled = false;
  } catch (error) {
    errorMessage.textContent =
      error instanceof Error ? error.message : "Ocurrió un error inesperado.";
    errorMessage.hidden = false;
  } finally {
    generateButton.disabled = false;
    generateButton.removeAttribute("aria-busy");
  }
}

async function copyPassword() {
  const password = passwordOutput.textContent;
  if (!password || password === "Pulsa generar") return;

  try {
    await navigator.clipboard.writeText(password);
    copyButton.setAttribute("aria-label", "Contraseña copiada");
    copyButton.title = "Copiada";
    window.setTimeout(() => {
      copyButton.setAttribute("aria-label", "Copiar contraseña");
      copyButton.title = "Copiar";
    }, 1600);
  } catch {
    errorMessage.textContent = "No se pudo copiar. Selecciona la contraseña para copiarla.";
    errorMessage.hidden = false;
  }
}

lengthSlider.addEventListener("input", updateSlider);
generateButton.addEventListener("click", generatePassword);
copyButton.addEventListener("click", copyPassword);
document.querySelectorAll('.option-row input[type="checkbox"]').forEach((input) => {
  input.addEventListener("change", () => {
    const anySelected = [...document.querySelectorAll('.option-row input[type="checkbox"]')].some(
      (option) => option.checked,
    );
    generateButton.disabled = !anySelected;
    errorMessage.textContent = anySelected ? "" : "Selecciona al menos un tipo de carácter.";
    errorMessage.hidden = anySelected;
  });
});
updateSlider();
generatePassword();
