function togglePassword() {
    const passwordInput = document.getElementById("loginpass");
    const toggleIcon = document.getElementById("togglePassword");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    }
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
