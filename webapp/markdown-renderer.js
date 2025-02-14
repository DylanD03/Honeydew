import { marked } from "marked"; // Import the markdown converter

// Handle rendering
window.addEventListener('load', () => {
    const contentDivs = document.querySelectorAll('.content'); // Select all elements with class 'content'

    contentDivs.forEach(contentDiv => {
        const markdownText = contentDiv.innerHTML;
        const htmlOutput = marked(markdownText);
        contentDiv.innerHTML = htmlOutput;
        contentDiv.style.display = 'block';
    });
});