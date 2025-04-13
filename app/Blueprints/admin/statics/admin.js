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

document.getElementById("selectAll").addEventListener("click", function () {
    const checkboxes = document.querySelectorAll(".alumni-checkbox");
    checkboxes.forEach((checkbox) => (checkbox.checked = true));
});

document.getElementById("deselectAll").addEventListener("click", function () {
    const checkboxes = document.querySelectorAll(".alumni-checkbox");
    checkboxes.forEach((checkbox) => (checkbox.checked = false));
});

document.getElementById("bulkApprove").addEventListener("click", function () {
    submitBulkAction("approve");
});

document.getElementById("bulkReject").addEventListener("click", function () {
    submitBulkAction("reject");
});

function submitBulkAction(action) {
    const form = document.getElementById("bulkActionForm");
    const selectedUsers = [
        ...document.querySelectorAll(".alumni-checkbox:checked"),
    ].map((cb) => cb.value);

    if (selectedUsers.length === 0) {
        alert("Please select at least one alumni");
        return;
    }

    const actionInput = document.createElement("input");
    actionInput.type = "hidden";
    actionInput.name = "action";
    actionInput.value = action;
    form.appendChild(actionInput);
    form.submit();
}