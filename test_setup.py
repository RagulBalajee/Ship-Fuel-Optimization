#!/usr/bin/env python3
"""
🚢 Ship Fuel Optimizer - Setup Testing Script
This script tests if all components are working correctly.
"""

import os
import sys
import sqlite3
import requests
import json
from pathlib import Path

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "SUCCESS": "✅",
        "ERROR": "❌", 
        "WARNING": "⚠️",
        "INFO": "ℹ️"
    }
    print(f"{colors.get(status, 'ℹ️')} {message}")

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        "backend/apps.py",
        "backend/requirements.txt", 
        "backend/ports.db",
        "frontend/index.html",
        "frontend/styles.css",
        "frontend/script.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print_status(f"Found {file_path}", "SUCCESS")
        else:
            print_status(f"Missing {file_path}", "ERROR")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_database():
    """Test if the database is working and has data"""
    print("\n🗄️ Testing Database...")
    
    try:
        conn = sqlite3.connect("backend/ports.db")
        cursor = conn.cursor()
        
        # Check if ports table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ports'")
        if cursor.fetchone():
            print_status("Ports table exists", "SUCCESS")
        else:
            print_status("Ports table not found", "ERROR")
            return False
        
        # Check if there's data
        cursor.execute("SELECT COUNT(*) FROM ports")
        count = cursor.fetchone()[0]
        if count > 0:
            print_status(f"Database has {count} ports", "SUCCESS")
        else:
            print_status("Database is empty", "WARNING")
        
        # Test a sample query
        cursor.execute("SELECT name, latitude, longitude FROM ports LIMIT 3")
        sample_ports = cursor.fetchall()
        if sample_ports:
            print_status("Sample ports found", "SUCCESS")
            for port in sample_ports:
                print(f"   - {port[0]} ({port[1]}, {port[2]})")
        else:
            print_status("No sample ports found", "WARNING")
        
        conn.close()
        return True
        
    except Exception as e:
        print_status(f"Database error: {e}", "ERROR")
        return False

def test_backend_dependencies():
    """Test if backend dependencies can be imported"""
    print("\n🐍 Testing Backend Dependencies...")
    
    try:
        # Add backend to path
        sys.path.insert(0, 'backend')
        
        # Test imports
        import fastapi
        print_status("FastAPI imported successfully", "SUCCESS")
        
        import uvicorn
        print_status("Uvicorn imported successfully", "SUCCESS")
        
        import geopy
        print_status("Geopy imported successfully", "SUCCESS")
        
        import sqlite3
        print_status("SQLite3 imported successfully", "SUCCESS")
        
        return True
        
    except ImportError as e:
        print_status(f"Import error: {e}", "ERROR")
        print_status("Run: cd backend && pip install -r requirements.txt", "INFO")
        return False
    except Exception as e:
        print_status(f"Unexpected error: {e}", "ERROR")
        return False

def test_backend_api():
    """Test if the backend API is working"""
    print("\n🌐 Testing Backend API...")
    
    try:
        # Try to import the app
        sys.path.insert(0, 'backend')
        from apps import app
        
        print_status("FastAPI app imported successfully", "SUCCESS")
        
        # Test if we can create a test client
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test health check endpoint
        response = client.get("/")
        if response.status_code == 200:
            print_status("Health check endpoint working", "SUCCESS")
        else:
            print_status(f"Health check failed: {response.status_code}", "ERROR")
            return False
        
        # Test ports endpoint
        response = client.get("/ports/")
        if response.status_code == 200:
            data = response.json()
            print_status(f"Ports endpoint working ({len(data)} ports)", "SUCCESS")
        else:
            print_status(f"Ports endpoint failed: {response.status_code}", "ERROR")
            return False
        
        return True
        
    except Exception as e:
        print_status(f"API test error: {e}", "ERROR")
        return False

def test_frontend_files():
    """Test if frontend files are valid"""
    print("\n🎨 Testing Frontend Files...")
    
    # Test HTML file
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            if "<!DOCTYPE html>" in html_content:
                print_status("HTML file is valid", "SUCCESS")
            else:
                print_status("HTML file seems invalid", "WARNING")
    except Exception as e:
        print_status(f"HTML file error: {e}", "ERROR")
        return False
    
    # Test CSS file
    try:
        with open("frontend/styles.css", "r", encoding="utf-8") as f:
            css_content = f.read()
            if len(css_content) > 100:  # Basic check
                print_status("CSS file is valid", "SUCCESS")
            else:
                print_status("CSS file seems too small", "WARNING")
    except Exception as e:
        print_status(f"CSS file error: {e}", "ERROR")
        return False
    
    # Test JavaScript file
    try:
        with open("frontend/script.js", "r", encoding="utf-8") as f:
            js_content = f.read()
            if "API_BASE_URL" in js_content:
                print_status("JavaScript file is valid", "SUCCESS")
            else:
                print_status("JavaScript file seems invalid", "WARNING")
    except Exception as e:
        print_status(f"JavaScript file error: {e}", "ERROR")
        return False
    
    return True

def test_local_server():
    """Test if local server can be started"""
    print("\n🚀 Testing Local Server...")
    
    try:
        import subprocess
        import time
        
        # Try to start the server in background
        print_status("Attempting to start local server...", "INFO")
        
        # Check if port 8000 is already in use
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        
        if result == 0:
            print_status("Port 8000 is already in use (server might be running)", "WARNING")
            return True
        
        # Try to start server (non-blocking)
        process = subprocess.Popen(
            ["python", "-m", "uvicorn", "apps:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd="backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print_status("Local server started successfully", "SUCCESS")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print_status(f"Server failed to start: {stderr.decode()}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Server test error: {e}", "ERROR")
        return False

def main():
    """Run all tests"""
    print("🚢 Ship Fuel Optimizer - Setup Testing")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Database", test_database),
        ("Backend Dependencies", test_backend_dependencies),
        ("Backend API", test_backend_api),
        ("Frontend Files", test_frontend_files),
        ("Local Server", test_local_server)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Test '{test_name}' crashed: {e}", "ERROR")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print_status("🎉 All tests passed! Your setup is working correctly.", "SUCCESS")
        print("\n🚀 Next steps:")
        print("1. Start backend: cd backend && uvicorn apps:app --reload")
        print("2. Open frontend/index.html in your browser")
        print("3. Test the application!")
    else:
        print_status("⚠️ Some tests failed. Check the errors above.", "WARNING")
        print("\n🔧 Common fixes:")
        print("1. Install dependencies: cd backend && pip install -r requirements.txt")
        print("2. Check if all files are in the correct locations")
        print("3. Make sure the database file exists")

if __name__ == "__main__":
    main() 