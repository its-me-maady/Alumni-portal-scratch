function add_event() {
    document.getElementById("eventPopup").style.display = "block";
    document.body.classList.add("no-scroll");
}

function closeEventPopup() {
    document.getElementById("eventPopup").style.display = "none";
    document.body.classList.remove("no-scroll");
}