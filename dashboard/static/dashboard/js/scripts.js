document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="columns"]');
    const reportButtonContainer = document.getElementById('report-button-container');

    function toggleReportButton() {
        const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
        if (checkedCount >= 2) {
            reportButtonContainer.style.display = 'flex';
        } else {
            reportButtonContainer.style.display = 'none';
        }
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', toggleReportButton);
    });

    // Check on page load
    toggleReportButton();

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
      setTimeout(() => {
        alert.style.transition = "opacity 0.5s ease-out";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500);
      }, 4000);
    });
});