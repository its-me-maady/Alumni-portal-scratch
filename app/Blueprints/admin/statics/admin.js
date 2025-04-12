function openEventPopup() {
    document.getElementById("eventAddPopup").style.display = "block";
    document.body.classList.add("no-scroll");
}

function closeEventPopup() {
    document.getElementById("eventAddPopup").style.display = "none";
    document.body.classList.remove("no-scroll");
}

function openEventEdit(eventId) {
    document.getElementById("event-edit-title").value =
        eventId.getAttribute("data-title");
    document.getElementById("event-edit-description").value =
        eventId.getAttribute("data-description");
    document.getElementById("event-edit-date").value =
        eventId.getAttribute("data-date");
    document.getElementById("event-edit-form").action =
        "/admin/event-edit/" + eventId.getAttribute("data-id");
    document.getElementById("event-edit").style.display = "block";
    document.body.classList.add("no-scroll");
}

function closeEventEdit() {
    document.getElementById("event-edit").style.display = "none";
    document.body.classList.remove("no-scroll");
}
