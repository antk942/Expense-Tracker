document.addEventListener('DOMContentLoaded', function() {
    // Import functionality
    document.getElementById("import-button").addEventListener("click", function(event) {
        document.getElementById("excel-file").click();
    });

    document.getElementById("excel-file").addEventListener("change", function(event) {
        document.getElementById("import-progress-bar").style.display = "block";

        var formData = new FormData();
        formData.append("excel_file", event.target.files[0]);
        formData.append("csrfmiddlewaretoken", csrfToken);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", importUrl, true);

        xhr.onload = function() {
            document.getElementById("import-progress-bar").style.display = "none";

            if (xhr.status === 200) {
                alert("Expenses imported successfully!");
                window.location.reload();
            } else {
                alert("Error importing expenses. Please try again.");
            }
        };

        xhr.send(formData);
    });

    // Export functionality
    document.getElementById("export-button").addEventListener("click", function(event) {
        event.preventDefault();
        document.getElementById("export-progress-bar").style.display = "block";

        var xhr = new XMLHttpRequest();
        xhr.open("GET", exportUrl, true);
        xhr.responseType = 'blob';

        xhr.onload = function() {
            document.getElementById("export-progress-bar").style.display = "none";

            if (xhr.status === 200) {
                var blob = xhr.response;
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = "expenses_export.xlsx";
                link.click();
            } else {
                alert("Error exporting expenses. Please try again.");
            }
        };

        xhr.send();
    });
});
