#!/bin/bash

# 🚀 Ship Fuel Optimizer Deployment Script
# This script helps you deploy your application

echo "🚢 Ship Fuel Optimizer Deployment Helper"
echo "========================================"

echo ""
echo "📋 Available Deployment Options:"
echo "1. Deploy Backend to Render"
echo "2. Deploy Frontend to Netlify"
echo "3. Deploy Both (Manual Steps)"
echo "4. Test Local Setup"
echo "5. Exit"

read -p "Choose an option (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🌐 Deploying Backend to Render..."
        echo ""
        echo "📝 Steps to deploy backend to Render:"
        echo "1. Go to https://render.com and sign up"
        echo "2. Click 'New +' → 'Web Service'"
        echo "3. Connect your GitHub repository: https://github.com/RagulBalajee/Ship-Fuel-Optimization"
        echo "4. Configure settings:"
        echo "   - Name: ship-fuel-optimizer-backend"
        echo "   - Environment: Python 3"
        echo "   - Build Command: pip install -r backend/requirements.txt"
        echo "   - Start Command: cd backend && uvicorn apps:app --host 0.0.0.0 --port \$PORT"
        echo "5. Click 'Create Web Service'"
        echo "6. Wait for deployment and copy the URL"
        echo ""
        echo "🔗 Your backend will be available at: https://your-app.onrender.com"
        ;;
    2)
        echo ""
        echo "🌐 Deploying Frontend to Netlify..."
        echo ""
        echo "📝 Steps to deploy frontend to Netlify:"
        echo "1. Go to https://netlify.com and sign up"
        echo "2. Drag and drop the 'frontend' folder to deploy"
        echo "   OR"
        echo "3. Connect your GitHub repository and set:"
        echo "   - Build command: (leave empty)"
        echo "   - Publish directory: frontend"
        echo ""
        echo "🔗 Your frontend will be available at: https://your-site.netlify.app"
        echo ""
        echo "⚠️  IMPORTANT: After deployment, update the API_BASE_URL in frontend/script.js"
        ;;
    3)
        echo ""
        echo "🚀 Deploying Both Frontend and Backend..."
        echo ""
        echo "📋 Complete Deployment Guide:"
        echo ""
        echo "STEP 1: Deploy Backend to Render"
        echo "1. Go to https://render.com"
        echo "2. Create new Web Service"
        echo "3. Connect GitHub repo: https://github.com/RagulBalajee/Ship-Fuel-Optimization"
        echo "4. Configure:"
        echo "   - Build: pip install -r backend/requirements.txt"
        echo "   - Start: cd backend && uvicorn apps:app --host 0.0.0.0 --port \$PORT"
        echo "5. Deploy and copy the URL"
        echo ""
        echo "STEP 2: Update Frontend API URL"
        echo "1. Edit frontend/script.js"
        echo "2. Change line 2 to your Render URL:"
        echo "   const API_BASE_URL = 'https://your-app.onrender.com';"
        echo ""
        echo "STEP 3: Deploy Frontend to Netlify"
        echo "1. Go to https://netlify.com"
        echo "2. Drag and drop 'frontend' folder"
        echo "3. Your site will be live!"
        ;;
    4)
        echo ""
        echo "🧪 Testing Local Setup..."
        echo ""
        
        # Check if backend is running
        if curl -s http://127.0.0.1:8000/ > /dev/null; then
            echo "✅ Backend is running at http://127.0.0.1:8000"
        else
            echo "❌ Backend is not running"
            echo "   Start it with: cd backend && uvicorn apps:app --reload"
        fi
        
        # Check if frontend files exist
        if [ -f "frontend/index.html" ]; then
            echo "✅ Frontend files found"
        else
            echo "❌ Frontend files not found"
        fi
        
        # Check if database exists
        if [ -f "backend/ports.db" ]; then
            echo "✅ Database file found"
        else
            echo "❌ Database file not found"
        fi
        
        echo ""
        echo "🌐 To test locally:"
        echo "1. Start backend: cd backend && uvicorn apps:app --reload"
        echo "2. Open frontend/index.html in your browser"
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option. Please choose 1-5."
        ;;
esac

echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
echo "🔗 Your GitHub repo: https://github.com/RagulBalajee/Ship-Fuel-Optimization" 