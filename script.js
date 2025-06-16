function getRoute() {
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;
    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    if (!start || !destination) {
        showError("Please enter both departure and destination ports.");
        return;
    }

    // Show loading spinner
    loader.style.display = "block";
    resultDiv.innerHTML = "";

    fetch(`http://127.0.0.1:8000/route?start=${start}&destination=${destination}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                resultDiv.innerHTML = `
                    <p><i class="fas fa-map-marker-alt"></i> Departure: ${data.start_port}</p>
                    <p><i class="fas fa-map-pin"></i> Destination: ${data.destination_port}</p>
                    <p><i class="fas fa-road"></i> Distance: ${data.distance_km} km</p>
                    <p><i class="fas fa-gas-pump"></i> Fuel Required: ${data.fuel_required_tons} tons</p>
                `;
            }
        })
        .catch(error => {
            showError("Failed to connect to optimization server. Please try again later.");
        })
        .finally(() => {
            loader.style.display = "none";
        });
}

function showError(message) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <p style="color: #dc3545; border-left-color: #dc3545;">
            <i class="fas fa-exclamation-triangle"></i> ${message}
        </p>
    `;
}