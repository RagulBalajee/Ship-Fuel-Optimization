#!/usr/bin/env python3

import os
import sys
import sqlite3

def test_database():
    """Test database connection and basic queries"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ports.db")
        print(f"Database path: {db_path}")
        print(f"Database exists: {os.path.exists(db_path)}")
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT COUNT(*) FROM ports")
            count = cursor.fetchone()[0]
            print(f"Number of ports in database: {count}")
            
            # Test states query
            cursor.execute("SELECT DISTINCT country FROM ports WHERE country IS NOT NULL AND country != '' LIMIT 5")
            states = cursor.fetchall()
            print(f"Sample states: {[s[0] for s in states]}")
            
            conn.close()
            return True
        else:
            print("Database file not found!")
            return False
    except Exception as e:
        print(f"Database error: {e}")
        return False

def test_imports():
    """Test all required imports"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import geopy.distance
        print("✅ Geopy imported successfully")
        
        import pandas
        print("✅ Pandas imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test app creation"""
    try:
        from apps import app
        print("✅ App imported successfully")
        
        # Test basic app functionality
        print(f"App title: {app.title}")
        print(f"App version: {app.version}")
        
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def main():
    print("🔍 Testing Ship Fuel Optimizer Server...")
    print("=" * 50)
    
    # Test imports
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    # Test database
    print("\n2. Testing database...")
    db_ok = test_database()
    
    # Test app creation
    print("\n3. Testing app creation...")
    app_ok = test_app_creation()
    
    print("\n" + "=" * 50)
    if imports_ok and db_ok and app_ok:
        print("✅ All tests passed! Server should work.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 