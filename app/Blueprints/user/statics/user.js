window.onload = function () {
    setTimeout(function () {
        openPopup();
    }, 500);
};

function openPopup() {
    document.getElementById("popupForm").style.display = "block";
    document.body.classList.add("popup-open");
}

function closePopup() {
    document.getElementById("popupForm").style.display = "none";
    document.body.classList.remove("popup-open");
}
