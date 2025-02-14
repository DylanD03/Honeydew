/* This code was taken from:
    Authors: Azimi A, Abdelghany MA, Qi W
    Date: 05/09/2024
    Title: Django Lab
    Availble at: https://uofa-cmput404.github.io/labsignments/django.html#adding-markdown-editor
*/

import { marked } from "marked"; // Import the markdown converter

// Handle Markdown conversion and rendering
document.getElementById('convert-btn').addEventListener('click', e => {
  e.preventDefault();   // Prevents native functionality for this event
  const markdownText = document.getElementById('markdown-editor').value;
  const htmlOutput = marked(markdownText); // Convert markdown to HTML
  document.getElementById('markdown-output').innerHTML = htmlOutput; // Add the generated HTML code to the output div element
});