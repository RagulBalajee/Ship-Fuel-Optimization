// API Configuration - Change this URL based on your backend deployment
const API_BASE_URL = 'https://your-backend-url.onrender.com'; // Change this to your deployed backend URL
// For local development, use: 'http://127.0.0.1:8000'

// Tab Navigation
function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Clear previous results
    document.getElementById('result').innerHTML = '';
}

// Country code mapping for user reference
const countryCodeMap = {
    'USA': 'United States',
    'CAN': 'Canada', 
    'MX': 'Mexico',
    'GBR': 'United Kingdom',
    'FRA': 'France',
    'DEU': 'Germany',
    'NLD': 'Netherlands',
    'JPN': 'Japan',
    'KOR': 'South Korea',
    'CHN': 'China',
    'AUS': 'Australia',
    'NZL': 'New Zealand'
};

// Quick route selection for states
function setQuickRoute(states) {
    document.getElementById('states-input').value = states;
    
    // Show user-friendly message
    const stateNames = states.split(',').map(code => countryCodeMap[code.trim()] || code.trim()).join(', ');
    showInfo(`Selected: ${stateNames}`);
}

// Show info message
function showInfo(message) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <div class="route-result">
            <p style="color: #28a745; border-left-color: #28a745; margin: 0;">
                <i class="fas fa-info-circle"></i> ${message}
            </p>
        </div>
    `;
}

// Single Route Function
function getSingleRoute() {
    const start = document.getElementById("start").value;
    const destination = document.getElementById("destination").value;
    const shipType = document.getElementById("ship-type-single").value;
    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    if (!start || !destination) {
        showError("Please enter both departure and destination ports.");
        return;
    }

    // Show loading spinner
    loader.style.display = "block";
    resultDiv.innerHTML = "";

    fetch(`${API_BASE_URL}/route?start=${encodeURIComponent(start)}&destination=${encodeURIComponent(destination)}&ship_type=${shipType}`)
        .then(response => response.json())
        .then(data => {
            if (data.detail) {
                showError(data.detail);
            } else {
                displaySingleRouteResult(data);
            }
        })
        .catch(error => {
            showError("Failed to connect to optimization server. Please try again later.");
        })
        .finally(() => {
            loader.style.display = "none";
        });
}

// Multi-Port Route Function
function getMultiRoute() {
    const ports = document.getElementById("multi-ports").value;
    const shipType = document.getElementById("ship-type-multi").value;
    const optimize = document.getElementById("optimize-route").checked;
    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    if (!ports.trim()) {
        showError("Please enter at least 2 port names separated by commas.");
        return;
    }

    const portList = ports.split(',').map(p => p.trim()).filter(p => p);
    if (portList.length < 2) {
        showError("Please enter at least 2 port names.");
        return;
    }

    // Show loading spinner
    loader.style.display = "block";
    resultDiv.innerHTML = "";

    const params = new URLSearchParams({
        ports: ports,
        ship_type: shipType,
        optimize: optimize
    });

    fetch(`${API_BASE_URL}/route/multi?${params}`)
        .then(response => response.json())
        .then(data => {
            if (data.detail) {
                showError(data.detail);
            } else {
                displayMultiRouteResult(data);
            }
        })
        .catch(error => {
            showError("Failed to connect to optimization server. Please try again later.");
        })
        .finally(() => {
            loader.style.display = "none";
        });
}

// State Routes Function
function getStateRoutes() {
    const states = document.getElementById("states-input").value;
    const shipType = document.getElementById("ship-type-states").value;
    const portsPerState = document.getElementById("ports-per-state").value;
    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    if (!states.trim()) {
        showError("Please enter at least 2 states/countries separated by commas.");
        return;
    }

    const stateList = states.split(',').map(s => s.trim()).filter(s => s);
    if (stateList.length < 2) {
        showError("Please enter at least 2 states/countries.");
        return;
    }

    // Show loading spinner
    loader.style.display = "block";
    resultDiv.innerHTML = "";

    const params = new URLSearchParams({
        states: states,
        ship_type: shipType,
        ports_per_state: portsPerState
    });

    fetch(`${API_BASE_URL}/route/states?${params}`)
        .then(response => response.json())
        .then(data => {
            if (data.detail) {
                showError(data.detail);
            } else {
                displayStateRouteResult(data);
            }
        })
        .catch(error => {
            showError("Failed to connect to optimization server. Please try again later.");
        })
        .finally(() => {
            loader.style.display = "none";
        });
}

// Display Single Route Result
function displaySingleRouteResult(data) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <div class="route-result">
            <h3><i class="fas fa-route"></i> Route Optimization Complete</h3>
            <div class="route-summary">
                <div class="summary-item">
                    <h4>Distance</h4>
                    <p>${data.distance_km} km</p>
                </div>
                <div class="summary-item">
                    <h4>Fuel Required</h4>
                    <p>${data.fuel_required_tons} tons</p>
                </div>
                <div class="summary-item">
                    <h4>Ship Type</h4>
                    <p>${data.ship_type}</p>
                </div>
            </div>
            <div class="route-segments">
                <div class="segment">
                    <div class="segment-info">
                        <i class="fas fa-anchor"></i>
                        <span class="segment-route">${data.start_port} → ${data.destination_port}</span>
                    </div>
                    <div class="segment-details">
                        <span><i class="fas fa-road"></i> ${data.distance_km} km</span>
                        <span><i class="fas fa-gas-pump"></i> ${data.fuel_required_tons} tons</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Display Multi-Port Route Result
function displayMultiRouteResult(data) {
    const resultDiv = document.getElementById("result");
    
    let segmentsHtml = '';
    data.segments.forEach((segment, index) => {
        segmentsHtml += `
            <div class="segment">
                <div class="segment-info">
                    <i class="fas fa-${index === 0 ? 'anchor' : 'ship'}"></i>
                    <span class="segment-route">${segment.from} → ${segment.to}</span>
                </div>
                <div class="segment-details">
                    <span><i class="fas fa-road"></i> ${segment.distance_km} km</span>
                    <span><i class="fas fa-gas-pump"></i> ${segment.fuel_tons} tons</span>
                </div>
            </div>
        `;
    });

    resultDiv.innerHTML = `
        <div class="route-result">
            <h3><i class="fas fa-map-marked-alt"></i> Multi-Port Route Optimization</h3>
            <div class="route-summary">
                <div class="summary-item">
                    <h4>Total Distance</h4>
                    <p>${data.total_distance_km} km</p>
                </div>
                <div class="summary-item">
                    <h4>Total Fuel</h4>
                    <p>${data.total_fuel_tons} tons</p>
                </div>
                <div class="summary-item">
                    <h4>Ports Visited</h4>
                    <p>${data.route.length}</p>
                </div>
                <div class="summary-item">
                    <h4>Ship Type</h4>
                    <p>${data.ship_type}</p>
                </div>
            </div>
            <div class="route-segments">
                <h4><i class="fas fa-route"></i> Optimized Route: ${data.route.join(' → ')}</h4>
                ${segmentsHtml}
            </div>
        </div>
    `;
}

// Display State Route Result
function displayStateRouteResult(data) {
    const resultDiv = document.getElementById("result");
    
    let segmentsHtml = '';
    data.segments.forEach((segment, index) => {
        segmentsHtml += `
            <div class="segment">
                <div class="segment-info">
                    <i class="fas fa-${index === 0 ? 'anchor' : 'ship'}"></i>
                    <span class="segment-route">${segment.from} → ${segment.to}</span>
                </div>
                <div class="segment-details">
                    <span><i class="fas fa-road"></i> ${segment.distance_km} km</span>
                    <span><i class="fas fa-gas-pump"></i> ${segment.fuel_tons} tons</span>
                </div>
            </div>
        `;
    });

    // Convert country codes to readable names
    const stateNames = data.states.map(code => countryCodeMap[code] || code).join(', ');

    resultDiv.innerHTML = `
        <div class="route-result">
            <h3><i class="fas fa-globe-americas"></i> State-Based Route Planning</h3>
            <div class="route-summary">
                <div class="summary-item">
                    <h4>States Visited</h4>
                    <p>${data.states.length}</p>
                </div>
                <div class="summary-item">
                    <h4>Total Distance</h4>
                    <p>${data.total_distance_km} km</p>
                </div>
                <div class="summary-item">
                    <h4>Total Fuel</h4>
                    <p>${data.total_fuel_tons} tons</p>
                </div>
                <div class="summary-item">
                    <h4>Ports per State</h4>
                    <p>${data.ports_per_state}</p>
                </div>
            </div>
            <div class="route-segments">
                <h4><i class="fas fa-map"></i> States: ${stateNames}</h4>
                <h4><i class="fas fa-route"></i> Optimized Route: ${data.route.join(' → ')}</h4>
                ${segmentsHtml}
            </div>
        </div>
    `;
}

// Error Display Function
function showError(message) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <div class="route-result">
            <p style="color: #dc3545; border-left-color: #dc3545; margin: 0;">
                <i class="fas fa-exclamation-triangle"></i> ${message}
            </p>
        </div>
    `;
}

// Legacy function for backward compatibility
function getRoute() {
    getSingleRoute();
}