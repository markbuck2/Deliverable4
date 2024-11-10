document.addEventListener("DOMContentLoaded", () => {
    // Table sorting functionality
    const table = document.querySelector("table");
    if (table) {
        const headers = table.querySelectorAll("th");
        let currentColumnIndex = 0;
        let sortOrder = -1; // Start in descending order (best to worst)

        function sortTableByColumn(columnIndex) {
            const rows = Array.from(table.querySelectorAll("tbody tr"));

            // Toggle sort order if the same column is clicked
            if (columnIndex === currentColumnIndex) {
                sortOrder *= -1;
            } else {
                sortOrder = -1; // Reset to descending if a new column is clicked
                currentColumnIndex = columnIndex;
            }

            const sortedRows = rows.sort((a, b) => {
                const cellA = a.children[columnIndex].innerText;
                const cellB = b.children[columnIndex].innerText;
                const valueA = isNaN(cellA) ? cellA : parseFloat(cellA);
                const valueB = isNaN(cellB) ? cellB : parseFloat(cellB);

                if (valueA < valueB) return -1 * sortOrder;
                if (valueA > valueB) return 1 * sortOrder;
                return 0;
            });

            // Clear existing rows and re-append sorted rows
            const tbody = table.querySelector("tbody");
            tbody.innerHTML = ""; // Clear existing rows
            sortedRows.forEach(row => tbody.appendChild(row));

            // Update header indicators
            headers.forEach(h => h.classList.remove("sort-asc", "sort-desc"));
            headers[columnIndex].classList.add(sortOrder === 1 ? "sort-asc" : "sort-desc");
        }

        // Initial sort on the first column in descending order (best to worst)
        sortTableByColumn(0);

        // Add click event to each header for sorting
        headers.forEach((header, index) => {
            header.style.cursor = "pointer";
            header.addEventListener("click", () => sortTableByColumn(index));
        });
    }

    // Hover effect to expand images
    document.querySelectorAll("img").forEach((img) => {
        img.addEventListener("mouseenter", () => {
            img.style.transition = "transform 0.3s ease";
            img.style.transform = "scale(1.2)"; // Scale up to 120%
            img.style.boxShadow = "0px 6px 12px rgba(0, 0, 0, 0.2)"; // Add shadow effect
        });

        img.addEventListener("mouseleave", () => {
            img.style.transform = "scale(1)"; // Reset to original size
            img.style.boxShadow = "none"; // Remove shadow effect
        });
    });
});
