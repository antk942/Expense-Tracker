document.addEventListener('DOMContentLoaded', function() {
    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    // Populate year dropdowns
    const yearSelect = document.getElementById('year-select');
    const yearSelectMonthly = document.getElementById('year-select-monthly');
    for (let year = currentYear; year >= currentYear - 10; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.text = year;
        yearSelect.appendChild(option);
        yearSelectMonthly.appendChild(option.cloneNode(true));
    }
    yearSelect.value = currentYear;
    yearSelectMonthly.value = currentYear;

    // Populate month dropdown
    const monthSelect = document.getElementById('month-select');
    for (let month = 1; month <= 12; month++) {
        const option = document.createElement('option');
        option.value = month;
        option.text = new Date(0, month - 1).toLocaleString('default', { month: 'long' });
        monthSelect.appendChild(option);
    }
    monthSelect.value = currentMonth;

    let yearlyChart, monthlyChart;
    
    function parseDataValues(data) {
        return Object.keys(data).reduce((result, key) => {
            result[key] = parseFloat(data[key]);
            return result;
        }, {});
    }

    // Function to render yearly chart
    async function renderYearlyChart(year) {   
        var url = window.location.origin; 
        const response = await fetch(`${url}/api/yearly-expenses/${year}/`);
        if (!response.ok) {
            throw new Error('Network response error');
        }
        let data = await response.json();

        // Parse the data values to numbers
        data = parseDataValues(data);

        // Calculate total expenses
        const total = Object.values(data).reduce((sum, value) => sum + value, 0);
        document.getElementById('yearly-total').textContent = total.toFixed(2);

        // Calculate percentages
        const percentageData = Object.keys(data).reduce((result, key) => {
            result[key] = (data[key] / total) * 100;
            return result;
        }, {});
        
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const labels = Object.keys(percentageData).map(month => monthNames[month - 1]);
        const colors = generateRandomColors(labels.length)

        const ctx = document.getElementById('yearlyChart').getContext('2d');
        if (yearlyChart) yearlyChart.destroy(); 
        yearlyChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: Object.values(percentageData),
                    backgroundColor: colors,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, 
                layout: {
                    padding: {
                        left: 0,
                        right: 0,
                        top: 0,
                        bottom: 100
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });        
    }

    // Function to render monthly chart
    async function renderMonthlyChart(year, month) {
        var url = window.location.origin; 
        const response = await fetch(`${url}/api/monthly-expenses/${year}/${month}`);
        if (!response.ok) {
            throw new Error('Network response error');
        }
        let data = await response.json();

        // Parse the data values to numbers
        data = parseDataValues(data);

        // Calculate total expenses
        const total = Object.values(data).reduce((sum, value) => sum + value, 0);
        document.getElementById('monthly-total').textContent = total.toFixed(2);

        // Calculate percentages
        const percentageData = Object.keys(data).reduce((result, key) => {
            result[key] = (data[key] / total) * 100;
            return result;
        }, {});
        
        const colors = generateRandomColors(Object.keys(data).length)

        const ctx = document.getElementById('monthlyChart').getContext('2d');
        if (monthlyChart) monthlyChart.destroy(); 
        monthlyChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(percentageData),
                datasets: [{
                    data: Object.values(percentageData),
                    backgroundColor: colors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, 
                layout: {
                    padding: {
                        left: 0,
                        right: 0,
                        top: 0,
                        bottom: 100
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    // Initial render
    renderYearlyChart(currentYear);
    renderMonthlyChart(currentYear, currentMonth);

    // Event listeners for dropdowns
    yearSelect.addEventListener('change', function() {
        renderYearlyChart(this.value);
    });

    yearSelectMonthly.addEventListener('change', function() {
        renderMonthlyChart(this.value, monthSelect.value);
    });

    monthSelect.addEventListener('change', function() {
        renderMonthlyChart(yearSelectMonthly.value, this.value);
    });
});

// Function to generate random colors
function generateRandomColors(count, saturation = 70, lightness = 50) {
    const colors = [];
    const hueStep = 360 / count;  // Divide the hue range by the number of colors needed

    for (let i = 0; i < count; i++) {
        const hue = i * hueStep;  // Generate evenly spaced hues
        colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
    }

    return colors;
}

document.addEventListener('DOMContentLoaded', function() {
    const monthlyTotal = document.getElementById('monthly-total');
    const yearlyTotal = document.getElementById('yearly-total');
    const toggleMonthlyIcon = document.getElementById('toggle-monthly-total');
    const toggleYearlyIcon = document.getElementById('toggle-yearly-total');

    toggleMonthlyIcon.addEventListener('click', function() {
        if (monthlyTotal.classList.contains('blurred')) {
            monthlyTotal.classList.remove('blurred');
            toggleMonthlyIcon.classList.remove('fa-eye');
            toggleMonthlyIcon.classList.add('fa-eye-slash');
        } else {
            monthlyTotal.classList.add('blurred');
            toggleMonthlyIcon.classList.remove('fa-eye-slash');
            toggleMonthlyIcon.classList.add('fa-eye');
        }
    });

    toggleYearlyIcon.addEventListener('click', function() {
        if (yearlyTotal.classList.contains('blurred')) {
            yearlyTotal.classList.remove('blurred');
            toggleYearlyIcon.classList.remove('fa-eye');
            toggleYearlyIcon.classList.add('fa-eye-slash');
        } else {
            yearlyTotal.classList.add('blurred');
            toggleYearlyIcon.classList.remove('fa-eye-slash');
            toggleYearlyIcon.classList.add('fa-eye');
        }
    });
});
