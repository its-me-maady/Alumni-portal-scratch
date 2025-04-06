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

window.onload = function () {
    setTimeout(function () {
        openPopup();
    }, 500);
};

function openPopup() {
    document.getElementById("popupForm").style.display = "block";
    document.body.classList.add("no-scroll");
}

function add_event() {
    document.getElementById("eventPopup").style.display = "block";
    document.body.classList.add("no-scroll");
}

function closeEventPopup() {
    document.getElementById("eventPopup").style.display = "none";
    document.body.classList.remove("no-scroll");
}


