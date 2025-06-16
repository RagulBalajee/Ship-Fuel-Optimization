import pandas as pd
import os
import sqlite3

# Get absolute file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "port_data.csv")
db_file = os.path.join(script_dir, "ports.db")

print(f"Looking for CSV at: {csv_file}")

# Check if file exists before proceeding
if not os.path.exists(csv_file):
    print("Error: CSV file not found! Ensure port_data.csv is in the backend folder.")
    exit(1)

try:
    # Load CSV
    df = pd.read_csv(csv_file, encoding="ISO-8859-1")  # Handle special characters
    print("CSV file loaded successfully!")

    # Keep only required columns
    df.rename(columns={'PortName': 'name', 'Country': 'country', 'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)
    df = df[['name', 'country', 'latitude', 'longitude']].dropna()

    # Connect to SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        country TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );
    """)

    # Insert data into table
    df.to_sql("ports", conn, if_exists="replace", index=False)

    # Commit & close
    conn.commit()
    conn.close()

    print(f"✅ Successfully imported {len(df)} ports into SQLite!")

except Exception as e:
    print(f"Error: {e}")
