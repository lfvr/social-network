function like(message_id) {
    // Get div and edit button, hide edit button
    const div = document.getElementById("likes-" + message_id)
    const button = document.getElementById("likes-" + message_id).getElementsByTagName("button")[0]

    let incr = true
    // If change from like to unlike
    if (button.className == "liked") {
        incr = false;
    }
    // PUT request to update message
    fetch(('/like/' + message_id), {
        method: 'PUT',
        credentials : 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        return response.json();
    })
    .then(likes => {
        if (incr) {
            button.innerText = "❤️ " + likes.count;
            button.className = "liked";
        } else {
            button.innerText = "♡ " + likes.count;
            button.className = "not-liked";
        }
    })
    .catch(error => {
        console.log("error: " + error)
    })
}