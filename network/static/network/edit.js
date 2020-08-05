function edit(message_id) {
    // Get div and edit button, hide edit button
    const div = document.getElementById("message-" + message_id);
    var edit_button = document.getElementById("edit-button-" + message_id);
    edit_button.style.display = "none";

    // Create save button and add to DOM
    var save_button = document.createElement("button");
    save_button.className = "btn btn-primary save-button";
    save_button.id = ("save-button-" + message_id);
    save_button.innerHTML = "Save";
    edit_button.parentElement.appendChild(save_button);

    // Get and hide current messsage, populate text area with message, add text area to DOM
    var p = div.getElementsByTagName("p")[0]
    const message = p.innerHTML;
    var textarea = document.createElement("textarea");
    textarea.innerHTML = message;
    p.style.display = "none";
    div.appendChild(textarea);

    // Add event listener
    save_button.setAttribute("onclick", "save("+message_id+")")
}

function save(message_id) {
    // Get div, edit button, p and textarea, hide save button
    const div = document.getElementById("message-" + message_id);
    var edit_button = document.getElementById("edit-button-" + message_id);
    document.getElementById("save-button-" + message_id).remove();
    var p = div.getElementsByTagName("p")[0]
    var textarea = div.getElementsByTagName("textarea")[0];

    // Get message text
    const message = textarea.value;

    // PUT request to update message
    fetch(('/edit/' + message_id), {
        method: 'PUT',
        credentials : 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => {
        return response.json();
    })
    .catch(error => {
        console.log("error: " + error)
    })

    p.innerHTML = message;
    p.style.display = "";
    textarea.remove();
    edit_button.style.display = "";
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}