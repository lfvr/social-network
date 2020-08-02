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
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#follow").onsubmit = () => {

        // get values
        const button = document.querySelector("#follow_button");
        const request = new XMLHttpRequest();
        const is_following = button.value == "Unfollow";
        const profile = document.querySelector("#username").innerHTML;
        const followers = parseInt(document.querySelector("#followers").innerHTML);

        // open request
        request.open('POST', '/follow');
        request.setRequestHeader("X-CSRFToken", csrftoken)

        request.onload = () => {

            const data = JSON.parse(request.responseText);
            if (data.success) {
                if (is_following) {
                    // change button value and decrease follower count
                    button.value = "Follow";
                    document.querySelector("#followers").innerHTML = followers - 1;
                } else {
                    // change button value and increase follower count
                    button.value = "Unfollow";
                    document.querySelector("#followers").innerHTML = followers + 1;
                }
            } else {
                // error
                button.disabled = true;
            }
        }
        // Add data to send with request
        const data = new FormData();
        data.append('profile', profile);
        data.append('is_following', is_following)

        // send request
        request.send(data);
        return false;
    };
});