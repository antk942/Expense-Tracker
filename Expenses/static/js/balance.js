document.querySelectorAll('[id^="send-reminder-btn"]').forEach(button => {
    button.addEventListener('click', function() {
        var url = window.location.origin; 
        fetch(`${url}/sendReminderEmail/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.getElementById('csrf-token').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

document.querySelectorAll('[id^="mark-paid-btn"]').forEach(button => {
    button.addEventListener('click', function() {
        var url = window.location.origin; 
        const userId = this.parentElement.querySelector('.userId').value;
        fetch(`${url}/markExpensesPaid/${userId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.getElementById('csrf-token').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();  // Reload the page to reflect changes
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
