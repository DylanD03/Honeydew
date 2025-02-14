document.addEventListener("DOMContentLoaded", function () {
    // Select all share buttons, the share modal, close modal button, and submit share button
    const shareButton = document.getElementById("shareButton");
    const shareModal = document.getElementById('shareModal');
    const closeModal = document.getElementById('closeModal');
    const submitShare = document.getElementById('submitShare');

    // Select the form with the data attribute for post ID and extract the post ID
    const form = document.querySelector("form[data-post-id]");
    const postID = form.dataset.postId;

    // If the share button exists, add a click event listener to open the modal
    if (shareButton) {
        shareButton.addEventListener('click', () => {
            shareModal.style.display = 'block'; // Open the modal
        });
    }

    // If the close modal button exists, add a click event listener to close the modal
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            console.log("close btn clicked");  // Log to console
            shareModal.style.display = 'none'; // Close the modal
        });
    }
});

function copyLink() {
    /* This function copies the url of a post
       This fucntion was created by w3schools.com
       accessable at: https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
       accessed on: 2024-11-17
       */

    // Get the text field
    console.log("In copyLink")
    var copyText = document.getElementById("post_link");

    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);

    // Alert the copied text
    alert("Copied the text: " + copyText.value);
}

// Function to get the value of a specified cookie by name
function getCookie(name) {
    let cookieValue = null;
    // Check if cookies exist and are not empty
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim(); // Remove whitespace

            // If the cookie name matches, decode and return the cookie value
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue; // Return the found cookie value
}
