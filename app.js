async function createWeatherChart(latitude, longitude) {
    try {
      // Fetch data from the API
      const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=1`);
      const data = await response.json();
  
      // Extract time and temperature data
      const times = data.hourly.time.map(time => new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
      const temperatures = data.hourly.temperature_2m;
  
      // Generate dummy UV index data
      const uvIndex = temperatures.map(() => Math.random() * 10);
  
      // Get the canvas element
      const ctx = document.getElementById('tempChart').getContext('2d');
  
      // Create the chart
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: times,
          datasets: [
            {
              label: 'Temperature (°F)',
              data: temperatures,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
              yAxisID: 'y'
            },
            {
              label: 'UV Index',
              data: uvIndex,
              borderColor: 'rgb(255, 99, 132)',
              tension: 0.1,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          interaction: {
            mode: 'index',
            intersect: false,
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Time'
              }
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              title: {
                display: true,
                text: 'Temperature (°F)'
              }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              title: {
                display: true,
                text: 'UV Index'
              },
              grid: {
                drawOnChartArea: false,
              },
            }
          }
        }
      });
    } catch (error) {
      console.error('Error fetching or processing data:', error);
    }
  }
  
  // Call the function with desired latitude and longitude
  createWeatherChart(40.7128, -74.0060); // Example coordinates for New York City