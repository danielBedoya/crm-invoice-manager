document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="columns"]');
    const reportButtonContainer = document.getElementById('report-button-container');

    function toggleReportButton() {
        const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        if (checkedCount >= 2) {
            reportButtonContainer.style.display = 'block';
        } else {
            reportButtonContainer.style.display = 'none';
        }
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', toggleReportButton);
    });

    // Check on page load
    toggleReportButton();
});