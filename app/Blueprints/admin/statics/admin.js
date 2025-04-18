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

async function handlePopoverFormSubmit(e) {
    e.preventDefault();
    const selectedFields = [
        ...document.querySelectorAll(".download-checkbox:checked"),
    ].map((cb) => cb.value);

    if (selectedFields.length === 0) {
        alert("Please select at least one category to download");
        return;
    }

    const selectedUsers = [
        ...document.querySelectorAll(".alumni-checkbox:checked"),
    ].map((cb) => cb.value);

    if (selectedUsers.length === 0) {
        alert("Please select at least one alumni");
        return;
    }

    // Get the form element
    const form = document.getElementById("popoverForm");

    // Create and append selected users input
    selectedUsers.forEach((userId, index) => {
        const userInput = document.createElement("input");
        userInput.type = "hidden";
        userInput.name = "selected_users[]"; // Using array notation in name
        userInput.value = userId;
        form.appendChild(userInput);
    });

    // Create and append selected fields input
    selectedFields.forEach((field, index) => {
        const fieldInput = document.createElement("input");
        fieldInput.type = "hidden";
        fieldInput.name = "selected_fields[]"; // Using array notation in name
        fieldInput.value = field;
        form.appendChild(fieldInput);
    });

    // Submit the form
    form.submit();
    setTimeout(() => {
        window.location.reload();
    }, 1000);
}
