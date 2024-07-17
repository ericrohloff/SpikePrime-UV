document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('locationForm');
    const ctx = document.getElementById('uvChart').getContext('2d');
    let chart = null;

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const city = document.getElementById('city').value;
        const state = document.getElementById('state').value;
        
        const data = await fetchData(city, state);
        if (data) {
            if (chart) {
                chart.destroy(); // Destroy existing chart if it exists
            }
            chart = createChart(ctx, data); // Create new chart
        } else {
            alert('No data available for the specified location.');
        }
    });
});

async function fetchData(city, state) {
    try {
        const response = await fetch(`https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/CITY/${city}/STATE/${state}/JSON`);
        const data = await response.json();
        console.log('Fetched Data:', data); // Debugging step
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

function createChart(ctx, data) {
    // Extract labels and data points
    const labels = data.map(entry => moment(entry.DATE_TIME, 'MMM/DD/YYYY hh A').toDate());
    const uvIndex = data.map(entry => parseFloat(entry.UV_VALUE)); // Ensure values are numbers
    
    console.log('Labels:', labels); // Debugging step
    console.log('UV Index:', uvIndex); // Debugging step
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'UV Index',
                data: uvIndex,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        tooltipFormat: 'MMM DD, YYYY hh A',
                        displayFormats: {
                            hour: 'MMM DD, YYYY hh A'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date and Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'UV Index'
                    }
                }
            }
        }
    });
}
