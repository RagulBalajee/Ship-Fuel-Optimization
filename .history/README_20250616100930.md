# AI Ship Fuel Optimizer - State Route Planner

An advanced ship route optimization system that helps find the most fuel-efficient routes across multiple states, countries, and ports using AI-powered algorithms.

## 🚢 Features

### 1. **Single Port Route Planning**
- Calculate optimal routes between two specific ports
- Fuel consumption estimation based on ship type
- Distance calculation using geodesic formulas

### 2. **Multi-Port Route Optimization**
- Plan routes visiting multiple ports
- Automatic route optimization using nearest neighbor algorithm
- Detailed segment-by-segment fuel analysis
- Option to use custom port order or optimize automatically

### 3. **State-Based Route Planning** ⭐ **NEW**
- Plan routes across multiple states/countries
- Automatically select ports from each state
- Configurable number of ports per state
- Quick selection for popular regional routes:
  - North America (US, Canada, Mexico)
  - Western Europe (UK, France, Germany, Netherlands)
  - East Asia (Japan, South Korea, China)
  - Oceania (Australia, New Zealand)

### 4. **Ship Type Support**
- **Standard Ship**: 0.05 tons/km
- **Cargo Ship**: 0.07 tons/km
- **Tanker**: 0.09 tons/km
- **Passenger Ship**: 0.04 tons/km

## 🏗️ Architecture

### Backend (FastAPI)
- **`apps.py`**: Main API server with route optimization endpoints
- **`fetch_ports.py`**: Fetches port data from Overpass API
- **`import_ports.py`**: Imports port data from CSV to SQLite
- **`ports.db`**: SQLite database containing global port information

### Frontend (HTML/CSS/JavaScript)
- **`index.html`**: Modern tabbed interface
- **`styles.css`**: Responsive design with gradient animations
- **`script.js`**: Interactive route planning functionality

## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
pip install -r requirements.txt
python import_ports.py  # Import port data
uvicorn apps:app --reload  # Start API server
```

### 2. Open Frontend
```bash
cd frontend
# Open index.html in your browser
# Or serve with: python -m http.server 8080
```

### 3. Start Planning Routes
1. **Single Route**: Enter departure and destination ports
2. **Multi-Port**: Enter multiple ports separated by commas
3. **State Routes**: Enter states/countries and configure ports per state

## 📡 API Endpoints

### Core Routes
- `GET /` - Health check
- `GET /ports/` - List ports with pagination
- `GET /route` - Single port route optimization
- `GET /route/multi` - Multi-port route optimization
- `GET /route/states` - State-based route planning

### State Management
- `GET /states/` - List all available states/countries
- `GET /ports/by-state/{state}` - Get ports by state/country

## 🎯 Use Cases

### Maritime Logistics
- **Cargo Shipping**: Optimize routes for cargo vessels visiting multiple ports
- **Tanker Operations**: Plan fuel-efficient routes for oil tankers
- **Passenger Cruises**: Design optimal cruise itineraries

### Regional Planning
- **North American Routes**: Plan routes across US, Canada, and Mexico
- **European Operations**: Optimize routes across European countries
- **Asian Pacific**: Plan routes in the Asia-Pacific region

### Fleet Management
- **Multi-Vessel Operations**: Coordinate multiple ships efficiently
- **Fuel Budgeting**: Estimate fuel costs for route planning
- **Schedule Optimization**: Minimize travel time and fuel consumption

## 🔧 Technical Details

### Route Optimization Algorithm
- **Nearest Neighbor**: Greedy algorithm for route optimization
- **Geodesic Distance**: Accurate distance calculation using great circle formula
- **Fuel Efficiency**: Dynamic fuel consumption based on ship type

### Database Schema
```sql
CREATE TABLE ports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    country TEXT,
    latitude REAL,
    longitude REAL
);
```

### Data Sources
- **Port Data**: Global port database with coordinates and country information
- **Distance Calculation**: Geopy library for accurate geodesic distances
- **Real-time Updates**: Overpass API for additional port data

## 🎨 UI Features

### Modern Interface
- **Tabbed Navigation**: Easy switching between route types
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Gradient Animations**: Beautiful visual effects
- **Interactive Elements**: Hover effects and smooth transitions

### Result Display
- **Route Summary**: Key metrics at a glance
- **Segment Details**: Detailed breakdown of each route segment
- **Visual Icons**: Intuitive icons for different data types
- **Error Handling**: Clear error messages and validation

## 📊 Example Usage

### State-Based Route Planning
```
States: United States, Canada, Mexico
Ship Type: Cargo
Ports per State: 3

Result:
- Total Distance: 2,847 km
- Total Fuel: 199.3 tons
- States Visited: 3
- Optimized Route: Port A → Port B → Port C → ...
```

### Multi-Port Optimization
```
Ports: New York, London, Tokyo, Sydney
Ship Type: Passenger
Optimize: Yes

Result:
- Optimized Route: New York → London → Tokyo → Sydney
- Total Distance: 35,420 km
- Total Fuel: 1,416.8 tons
```

## 🔮 Future Enhancements

- **Weather Integration**: Consider weather conditions in route planning
- **Port Capacity**: Include port capacity and scheduling constraints
- **Real-time Tracking**: Live vessel tracking and route updates
- **Cost Analysis**: Include port fees, fuel prices, and operational costs
- **3D Visualization**: Interactive 3D map with route visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for the maritime industry** 