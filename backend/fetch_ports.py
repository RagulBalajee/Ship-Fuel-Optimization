import requests
import pandas as pd
import sqlite3

# Overpass API URL
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Overpass QL query to fetch global ports
QUERY = """
[out:json];
node["harbour"];
out body;
"""

def fetch_ports():
    response = requests.get(OVERPASS_URL, params={"data": QUERY}, timeout=60)

    if response.status_code == 200:
        data = response.json()
        ports = []

        for element in data.get("elements", []):
            if "name" in element and "lat" in element and "lon" in element:
                name = element["name"].strip()
                latitude = element["lat"]
                longitude = element["lon"]

                # Avoid duplicates by checking existing names
                ports.append((name, latitude, longitude))

        # Convert to DataFrame and drop duplicates
        df = pd.DataFrame(ports, columns=["name", "latitude", "longitude"])
        df = df.drop_duplicates(subset=["name"])  # Remove duplicate port names

        # Save to SQLite database
        conn = sqlite3.connect("/Users/ragulbalajee/Downloads/ship-fuel-optimizer/backend/ports.db")
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE, 
                latitude REAL, 
                longitude REAL
            )
        """)

        # Insert data, ignoring duplicates
        for _, row in df.iterrows():
            try:
                cursor.execute("INSERT INTO ports (name, latitude, longitude) VALUES (?, ?, ?)", 
                               (row["name"], row["latitude"], row["longitude"]))
            except sqlite3.IntegrityError:
                print(f"⚠️ Duplicate port found: {row['name']} (Skipping)")

        conn.commit()
        conn.close()

        print(f"✅ Successfully stored {len(df)} unique ports in 'ports.db'")

    else:
        print(f"❌ Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    fetch_ports()
