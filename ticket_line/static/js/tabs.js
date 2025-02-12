document.addEventListener("DOMContentLoaded", function () {
    const tabInputs = document.querySelectorAll(".tab-input");
    const tabContents = document.querySelectorAll(".tab-content");

    tabInputs.forEach(input => {
        input.addEventListener("change", function () {
            const targetTab = input.id.replace("-tab", "");
            tabContents.forEach(content => {
                if (content.id === targetTab) {
                    content.style.display = "block";
                } else {
                    content.style.display = "none";
                }
            });
        });
    });
});
