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
