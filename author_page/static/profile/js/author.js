document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("authorSearch");
    const authorList = document.getElementById("authorList");
    const authors = authorList.querySelectorAll("li");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase();
        authors.forEach(author => {
            const authorName = author.textContent.toLowerCase();
            if (authorName.includes(query)) {
                author.style.display = "";
            } else {
                author.style.display = "none";
            }
        });
    });
});
