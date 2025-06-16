import os
import sqlite3
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import geopy.distance

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
    distance = geopy.distance.geodesic(start_coords, destination_coords).km

    # Dynamic fuel efficiency based on ship type
    fuel_efficiency_map = {
        "standard": 0.05,  # 0.05 tons of fuel per km
        "cargo": 0.07,
        "tanker": 0.09,
        "passenger": 0.04,
    }
    fuel_efficiency = fuel_efficiency_map.get(ship_type.lower(), 0.05)
    fuel_required = round(distance * fuel_efficiency, 2)

    return {
        "start_port": start_details[0],
        "destination_port": destination_details[0],
        "distance_km": round(distance, 2),
        "fuel_required_tons": fuel_required,
        "ship_type": ship_type,
    }
