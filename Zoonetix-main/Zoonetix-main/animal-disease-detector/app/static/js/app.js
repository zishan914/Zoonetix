// Check if user is admin and show admin link
async function checkAdminStatus() {
  try {
    const response = await fetch('/api/user', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const user = await response.json();
      if (user.is_admin) {
        const adminLink = document.getElementById('adminLink');
        if (adminLink) {
          adminLink.style.display = 'block';
        }
      }
    }
  } catch (error) {
    console.error('Error checking admin status:', error);
  }
}

// Check admin status on page load
document.addEventListener('DOMContentLoaded', checkAdminStatus);

// Logout functionality
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/logout", {
        method: "POST",
      });
      if (response.ok) {
        window.location.href = "/";
      }
    } catch (error) {
      console.error("Logout error:", error);
    }
  });
}

const fileInput = document.getElementById("fileInput");
const previewShell = document.getElementById("previewShell");
const previewImage = document.getElementById("previewImage");
const previewText = document.getElementById("previewText");
const submitButton = document.getElementById("submitButton");
const uploadForm = document.getElementById("uploadForm");
const statusText = document.getElementById("statusText");
const resultDisease = document.getElementById("resultDisease");
const resultConfidence = document.getElementById("resultConfidence");
const resultMessage = document.getElementById("resultMessage");
const resultCard = document.getElementById("resultCard");
const treatmentCard = document.getElementById("treatmentCard");
const treatmentContent = document.getElementById("treatmentContent");
const treatmentDisclaimer = document.getElementById("treatmentDisclaimer");

let selectedFile = null;

function updateStatus(message, isError = false) {
  statusText.textContent = message;
  statusText.style.color = isError ? "#f66c6c" : "#b8c1d3";
}

function renderTreatment(treatment) {
  if (!treatment || !treatment.disease) {
    treatmentCard.classList.remove("visible");
    treatmentCard.style.display = "none";
    return;
  }

  const isHealthy = treatment.disease === "healthy";
  const urgencyClass = isHealthy ? "mild" : "";
  const urgencyIcon = isHealthy ? "✅" : "🚨";

  let medsHtml = "";
  if (treatment.medications && treatment.medications.length > 0 && treatment.medications[0].name !== "No medication needed") {
    medsHtml = `<div class="treatment-meds">` +
      treatment.medications.map(med =>
        `<div class="treatment-med">
          <strong>${med.name}</strong>
          <span>${med.type} — ${med.purpose}</span>
        </div>`
      ).join("") +
      `</div>`;
  } else {
    medsHtml = `<p style="color:var(--muted);margin:0;">No medication required. Keep up the good care!</p>`;
  }

  let precautionsHtml = "";
  if (treatment.precautions && treatment.precautions.length > 0) {
    precautionsHtml = `<ul>` +
      treatment.precautions.map(p => `<li>${p}</li>`).join("") +
      `</ul>`;
  }

  treatmentContent.innerHTML = `
    <div class="treatment-urgency ${urgencyClass}">
      <span>${urgencyIcon}</span>
      <span>${treatment.vet_urgency}</span>
    </div>

    <div class="treatment-section">
      <h4>📋 Symptoms</h4>
      <p>${treatment.symptoms}</p>
    </div>

    <div class="treatment-section">
      <h4>💊 Recommended Medications</h4>
      ${medsHtml}
    </div>

    <div class="treatment-section">
      <h4>📐 Dosage & Administration</h4>
      <p style="white-space:pre-line">${treatment.dosage_guide}</p>
    </div>

    <div class="treatment-section">
      <h4>🧴 How to Administer</h4>
      <p style="white-space:pre-line">${treatment.administration}</p>
    </div>

    <div class="treatment-section">
      <h4>⚠️ Precautions</h4>
      ${precautionsHtml}
    </div>

    <div class="treatment-section">
      <h4>🏠 Home Care</h4>
      <p>${treatment.home_care}</p>
    </div>

    <div class="treatment-section">
      <h4>🛡️ Prevention</h4>
      <p>${treatment.prevention}</p>
    </div>

    <div class="treatment-section">
      <h4>⏱️ Expected Recovery</h4>
      <p>${treatment.recovery_time}</p>
    </div>
  `;

  treatmentDisclaimer.textContent = treatment.disclaimer || "Always consult a licensed veterinarian before administering any medication.";
  treatmentCard.style.display = "block";
  // Force reflow for animation
  void treatmentCard.offsetWidth;
  treatmentCard.classList.add("visible");
}

fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (!file) {
    selectedFile = null;
    previewShell.classList.remove("visible");
    submitButton.disabled = true;
    updateStatus("Choose an image to start.");
    return;
  }

  if (!["image/jpeg", "image/png"].includes(file.type)) {
    updateStatus("Please choose a JPG or PNG image.", true);
    fileInput.value = "";
    selectedFile = null;
    previewShell.classList.remove("visible");
    submitButton.disabled = true;
    return;
  }

  selectedFile = file;
  previewImage.src = URL.createObjectURL(file);
  previewShell.classList.add("visible");
  previewText.textContent = file.name;
  submitButton.disabled = false;
  updateStatus("Image ready. Click Predict to send it to the API.");
});

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!selectedFile) {
    updateStatus("No file selected.", true);
    return;
  }

  submitButton.disabled = true;
  submitButton.classList.add("loading");
  submitButton.textContent = "Predicting...";
  updateStatus("Sending image to API...");

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let errorMessage = "Prediction failed.";
      const contentType = response.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        const error = await response.json();
        errorMessage = error.detail || error.message || errorMessage;
      } else {
        const text = await response.text();
        errorMessage = text || errorMessage;
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    resultDisease.textContent = data.disease;
    resultConfidence.textContent = `${(data.confidence * 100).toFixed(2)}%`;
    resultMessage.textContent = data.message;
    renderTreatment(data.treatment);
    updateStatus("Prediction complete.");
    resultCard.classList.add("pulse");
  } catch (err) {
    resultDisease.textContent = "—";
    resultConfidence.textContent = "—";
    resultMessage.textContent = err.message;
    updateStatus(err.message, true);
    resultCard.classList.add("pulse");
  } finally {
    submitButton.disabled = false;
    submitButton.classList.remove("loading");
    submitButton.textContent = "Predict disease";
    setTimeout(() => resultCard.classList.remove("pulse"), 900);
  }
});

window.addEventListener("DOMContentLoaded", () => {
  const heroCards = document.querySelectorAll(".hero-card");
  const heroDots = document.querySelectorAll(".hero-dot");
  let heroCardIndex = 0;

  if (heroCards.length === 0) return;

  function setActiveCard(index) {
    heroCards.forEach((card, cardIndex) => {
      card.classList.toggle("hero-card--active", cardIndex === index);
    });
    heroDots.forEach((dot, dotIndex) => {
      dot.classList.toggle("hero-dot--active", dotIndex === index);
    });
  }

  function rotateHeroCards() {
    heroCardIndex = (heroCardIndex + 1) % heroCards.length;
    setActiveCard(heroCardIndex);
  }

  heroDots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const index = Number(dot.dataset.index);
      if (!Number.isNaN(index)) {
        heroCardIndex = index;
        setActiveCard(heroCardIndex);
      }
    });
  });

  setActiveCard(heroCardIndex);
  setInterval(rotateHeroCards, 3200);
});
