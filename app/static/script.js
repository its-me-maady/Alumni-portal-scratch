function togglePassword() {
    const passwordInputs = document.querySelectorAll("#loginpass");
    const toggleIcons = document.querySelectorAll(".far");

    passwordInputs.forEach((input, index) => {
        if (input.type === "password") {
            input.type = "text";
            toggleIcons[index].classList.remove("fa-eye");
            toggleIcons[index].classList.add("fa-eye-slash");
        } else {
            input.type = "password";
            toggleIcons[index].classList.remove("fa-eye-slash");
            toggleIcons[index].classList.add("fa-eye");
        }
    });
}

function openPopup() {
    const popupForm = document.getElementById("popupForm");
    if (popupForm) {
        popupForm.style.display = "block";
        document.body.classList.add("no-scroll");
    }
}

const navbarToggle = document.querySelector(".navbar-toggle");
const navbarMenu = document.querySelector(".navbar-menu");

navbarToggle.addEventListener("click", () => {
    navbarMenu.classList.toggle("active");
});

function showEventDetails(eventId) {
    const eventDetails = document.getElementById("event-details");
    document.getElementById("event-title").textContent =
        eventId.getAttribute("data-title");
    document.getElementById("event-image").src =
        eventId.getAttribute("data-image");
    document.getElementById("event-description").textContent =
        eventId.getAttribute("data-description");
    document.getElementById("event-date").textContent =
        eventId.getAttribute("data-date");
    eventDetails.style.display = "block";
    document.body.classList.add("no-scroll");
}
function closeEventDetails() {
    const eventDetails = document.getElementById("event-details");
    eventDetails.style.display = "none";
    document.body.classList.remove("no-scroll");
}

document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert");
    const ANIMATION_DURATION = 500; // Duration of slide animation in ms
    const DISPLAY_DURATION = 5000; // How long to show the alert in ms

    alerts.forEach((alert) => {
        // Add close button to each alert
        const closeButton = document.createElement("button");
        closeButton.innerHTML = "&times;";
        closeButton.className = "alert-close";
        closeButton.addEventListener("click", () => dismissAlert(alert));
        alert.appendChild(closeButton);

        // Auto-dismiss after DISPLAY_DURATION
        setTimeout(() => dismissAlert(alert), DISPLAY_DURATION);
    });

    function dismissAlert(alert) {
        alert.classList.add("fade-out");
        setTimeout(() => {
            alert.remove();
        }, ANIMATION_DURATION);
    }
});
