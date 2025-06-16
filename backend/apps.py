import os
import sqlite3
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import geopy.distance
from typing import List, Dict, Any
import itertools

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Use the absolute path to `ports.db`
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ports.db")


# 🔹 Function to check if database exists
def check_database():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database file not found! Run `import_ports.py` first.")


# 🔹 Function to fetch port details
def get_port_details(port_name):
    check_database()  # Ensure database exists

    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT name, latitude, longitude FROM ports WHERE LOWER(name) = LOWER(?)", (port_name.lower(),))
        port = cursor.fetchone()
        conn.close()
        return port  # Returns (name, latitude, longitude) if found, else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


# 🔹 Function to calculate distance between two coordinates
def calculate_distance(coord1, coord2):
    return geopy.distance.geodesic(coord1, coord2).km


# 🔹 Function to calculate fuel consumption
def calculate_fuel(distance, ship_type="standard"):
    fuel_efficiency_map = {
        "standard": 0.05,  # 0.05 tons of fuel per km
        "cargo": 0.07,
        "tanker": 0.09,
        "passenger": 0.04,
    }
    fuel_efficiency = fuel_efficiency_map.get(ship_type.lower(), 0.05)
    return round(distance * fuel_efficiency, 2)


# 🔹 API to check if the server is running
@app.get("/")
def home():
    return {"message": "AI Ship Fuel Optimization API is Running!"}


# 🔹 API to fetch ports with pagination
@app.get("/ports/")
def get_ports(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    """
    Fetch ports with pagination.
    - `limit`: Number of ports to return (1-100)
    - `offset`: Number of ports to skip
    """
    check_database()  # Ensure database exists

    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, country, latitude, longitude FROM ports LIMIT ? OFFSET ?", (limit, offset)
        )
        ports = cursor.fetchall()
        conn.close()

        if not ports:
            return {"message": "No ports found in the database!"}

        return {"ports": [{"name": p[0], "country": p[1], "latitude": p[2], "longitude": p[3]} for p in ports]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


# 🔹 API to fetch ports by state/country
@app.get("/ports/by-state/{state}")
def get_ports_by_state(state: str, limit: int = Query(50, ge=1, le=200)):
    """
    Fetch ports filtered by state/country.
    - `state`: State or country name to filter by
    - `limit`: Maximum number of ports to return
    """
    check_database()

    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, country, latitude, longitude FROM ports WHERE LOWER(country) LIKE LOWER(?) LIMIT ?", 
            (f"%{state}%", limit)
        )
        ports = cursor.fetchall()
        conn.close()

        if not ports:
            return {"message": f"No ports found for state/country: {state}"}

        return {
            "state": state,
            "port_count": len(ports),
            "ports": [{"name": p[0], "country": p[1], "latitude": p[2], "longitude": p[3]} for p in ports]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


# 🔹 API to get all available states/countries
@app.get("/states/")
def get_states():
    """
    Get all available states/countries in the database.
    """
    check_database()

    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT country FROM ports WHERE country IS NOT NULL AND country != '' ORDER BY country")
        states = cursor.fetchall()
        conn.close()

        return {
            "states": [state[0] for state in states],
            "count": len(states)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


# 🔹 API for route optimization & fuel calculation
@app.get("/route")
def get_route(start: str, destination: str, ship_type: str = "standard"):
    """
    Get optimized route & fuel estimation.
    - `start`: Starting port name
    - `destination`: Destination port name
    - `ship_type`: Ship type for fuel efficiency (default: standard)
    """
    check_database()  # Ensure database exists

    start_details = get_port_details(start)
    destination_details = get_port_details(destination)

    if not start_details:
        raise HTTPException(status_code=400, detail=f"Start port '{start}' not found in database.")
    if not destination_details:
        raise HTTPException(status_code=400, detail=f"Destination port '{destination}' not found in database.")

    # Extract coordinates
    start_coords = (start_details[1], start_details[2])
    destination_coords = (destination_details[1], destination_details[2])

    # Calculate distance (in km)
    distance = calculate_distance(start_coords, destination_coords)
    fuel_required = calculate_fuel(distance, ship_type)

    return {
        "start_port": start_details[0],
        "destination_port": destination_details[0],
        "distance_km": round(distance, 2),
        "fuel_required_tons": fuel_required,
        "ship_type": ship_type,
    }


# 🔹 API for multi-port route optimization
@app.get("/route/multi")
def get_multi_route(ports: str, ship_type: str = "standard", optimize: bool = True):
    """
    Get optimized route for multiple ports.
    - `ports`: Comma-separated list of port names
    - `ship_type`: Ship type for fuel efficiency
    - `optimize`: Whether to optimize the route order (True) or use given order (False)
    """
    check_database()

    port_list = [p.strip() for p in ports.split(",") if p.strip()]
    
    if len(port_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 ports are required.")

    # Get port details for all ports
    port_details = []
    for port_name in port_list:
        details = get_port_details(port_name)
        if not details:
            raise HTTPException(status_code=400, detail=f"Port '{port_name}' not found in database.")
        port_details.append({
            "name": details[0],
            "coordinates": (details[1], details[2])
        })

    if optimize and len(port_details) > 2:
        # Use nearest neighbor algorithm for route optimization
        optimized_route = optimize_route(port_details)
    else:
        optimized_route = port_details

    # Calculate total distance and fuel
    total_distance = 0
    route_segments = []
    
    for i in range(len(optimized_route) - 1):
        current = optimized_route[i]
        next_port = optimized_route[i + 1]
        
        segment_distance = calculate_distance(current["coordinates"], next_port["coordinates"])
        segment_fuel = calculate_fuel(segment_distance, ship_type)
        
        total_distance += segment_distance
        route_segments.append({
            "from": current["name"],
            "to": next_port["name"],
            "distance_km": round(segment_distance, 2),
            "fuel_tons": segment_fuel
        })

    total_fuel = calculate_fuel(total_distance, ship_type)

    return {
        "route": [port["name"] for port in optimized_route],
        "total_distance_km": round(total_distance, 2),
        "total_fuel_tons": total_fuel,
        "ship_type": ship_type,
        "segments": route_segments,
        "optimized": optimize
    }


# 🔹 API for state-based route planning
@app.get("/route/states")
def get_state_routes(states: str, ship_type: str = "standard", ports_per_state: int = Query(3, ge=1, le=10)):
    """
    Plan routes across multiple states, visiting ports in each state.
    - `states`: Comma-separated list of states/countries
    - `ship_type`: Ship type for fuel efficiency
    - `ports_per_state`: Number of ports to visit per state
    """
    check_database()

    state_list = [s.strip() for s in states.split(",") if s.strip()]
    
    if len(state_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 states are required.")

    # Get ports for each state
    state_ports = {}
    for state in state_list:
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, latitude, longitude FROM ports WHERE LOWER(country) LIKE LOWER(?) LIMIT ?", 
                (f"%{state}%", ports_per_state)
            )
            ports = cursor.fetchall()
            conn.close()
            
            if ports:
                state_ports[state] = [
                    {"name": p[0], "coordinates": (p[1], p[2])} for p in ports
                ]
            else:
                raise HTTPException(status_code=400, detail=f"No ports found for state: {state}")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Create route visiting each state
    route = []
    for state in state_list:
        if state in state_ports:
            route.extend(state_ports[state])

    # Optimize the route
    optimized_route = optimize_route(route)

    # Calculate total distance and fuel
    total_distance = 0
    route_segments = []
    
    for i in range(len(optimized_route) - 1):
        current = optimized_route[i]
        next_port = optimized_route[i + 1]
        
        segment_distance = calculate_distance(current["coordinates"], next_port["coordinates"])
        segment_fuel = calculate_fuel(segment_distance, ship_type)
        
        total_distance += segment_distance
        route_segments.append({
            "from": current["name"],
            "to": next_port["name"],
            "distance_km": round(segment_distance, 2),
            "fuel_tons": segment_fuel
        })

    total_fuel = calculate_fuel(total_distance, ship_type)

    return {
        "states": state_list,
        "route": [port["name"] for port in optimized_route],
        "total_distance_km": round(total_distance, 2),
        "total_fuel_tons": total_fuel,
        "ship_type": ship_type,
        "segments": route_segments,
        "ports_per_state": ports_per_state
    }


# 🔹 Function to optimize route using nearest neighbor algorithm
def optimize_route(ports):
    """
    Optimize route using nearest neighbor algorithm.
    """
    if len(ports) <= 2:
        return ports
    
    unvisited = ports[1:]  # Start from second port
    current = ports[0]
    optimized = [current]
    
    while unvisited:
        # Find nearest unvisited port
        nearest = min(unvisited, key=lambda p: calculate_distance(current["coordinates"], p["coordinates"]))
        optimized.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return optimized
