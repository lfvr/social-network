function like(message_id) {
    // Get div and edit button, hide edit button
    const div = document.getElementById("likes-" + message_id)
    const button = document.getElementById("likes-" + message_id).getElementsByTagName("button")

    let incr = true
    // If change from like to unlike
    if (button.className == "liked") {
        incr = false;
    }
    // PUT request to update message
    fetch(('/like/' + message_id + "/" + incr), {
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
            button[0].innerText = "❤️ " + likes.count;
            button[0].className = "liked";
        } else {
            button[0].innerText = "♡ " + likes.count;
            button[0].className = "not-liked";
        }
    })
    .catch(error => {
        console.log("error: " + error)
    })
}