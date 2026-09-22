
const $ = (id) => document.getElementById(id);

document.addEventListener("DOMContentLoaded", () => {
  const length = $("length");
  const lengthValue = $("lengthValue");
  const generateBtn = $("generateBtn");
  const password = $("password");
  const strength = $("strength");
  const meter = $("meter");
  const kat = $("kat");
  const bhutaResult = $("bhutaResult");
  const checks = $("checks");
  const copyBtn = $("copyBtn");

  length.addEventListener("input", () => lengthValue.textContent = length.value);

  async function generate() {
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';

    try {
      const response = await fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          word: $("word").value,
          bhuta: $("bhuta").value,
          length: Number(length.value)
        })
      });
      const data = await response.json();

      password.textContent = data.password;
      strength.textContent = data.strength;
      kat.textContent = data.katapayadi;
      bhutaResult.textContent = `${data.bhuta_name} → ${data.bhuta_value}`;

      const pct = data.strength === "Strong" ? 100 : data.strength === "Medium" ? 65 : 35;
      meter.style.width = pct + "%";

      checks.innerHTML = Object.entries(data.checks).map(([label, ok]) =>
        `<div class="check ${ok ? "ok" : ""}"><i class="bi ${ok ? "bi-check-circle-fill" : "bi-circle"}"></i>${label}</div>`
      ).join("");
    } catch (err) {
      password.textContent = "Could not generate. Start Flask and try again.";
      strength.textContent = "—";
    } finally {
      generateBtn.disabled = false;
      generateBtn.innerHTML = '<i class="bi bi-magic"></i> Generate Secure Password';
    }
  }

  generateBtn.addEventListener("click", generate);
  copyBtn.addEventListener("click", async () => {
    const value = password.textContent;
    if (!value || value === "Click Generate") return;
    await navigator.clipboard.writeText(value);
    copyBtn.innerHTML = '<i class="bi bi-check2"></i>';
    setTimeout(() => copyBtn.innerHTML = '<i class="bi bi-copy"></i>', 1200);
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, {threshold: 0.12});
  document.querySelectorAll(".reveal").forEach(el => observer.observe(el));
});
