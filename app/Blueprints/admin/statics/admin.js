function openEventPopup() {
    document.getElementById("eventAddPopup").style.display = "block";
    document.body.classList.add("no-scroll");
}

function closeEventPopup() {
    document.getElementById("eventAddPopup").style.display = "none";
    document.body.classList.remove("no-scroll");
}
