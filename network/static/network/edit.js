function edit(message_id) {
    div = document.getElementById("message-" + message_id);
    button = document.getElementById("edit-button-" + message_id);
    button.className = "btn btn-primary edit-button";
    button.innerHTML = "Save";
    message = div.children[0].innerHTML;
    textarea = document.createElement("textarea");
    textarea.innerHTML = message;
    div.children[0].style.display = "none";
    div.appendChild(textarea);
}