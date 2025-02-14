document.addEventListener("DOMContentLoaded", function () {
    console.log("comment.js loaded");
    // Get the comment modal elements
    //const commentButton = document.getElementById("commentButton");
    const commentModal = document.getElementById("commentModal");
    const closeModal = document.getElementById('closeCommentModal');
    

     // Use event delegation to handle comment buttons
     document.addEventListener('click', function(event) {
        // Check if the clicked element is a comment button
        const commentButton = event.target.closest('.commentButton');
        if (commentButton) {
            console.log("comment button clicked");
            commentModal.style.display = 'block'; // Open the modal
        }
    });
    
    // If the close modal button exists, add a click event listener to close the modal
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            console.log("close btn clicked");  // Log to console
            commentModal.style.display = 'none'; // Close the modal
        });
    }
});