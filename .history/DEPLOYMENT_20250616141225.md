# 🚀 Deployment Guide - Ship Fuel Optimizer

This guide explains how to deploy your Ship Fuel Optimizer to different platforms.

## 📋 **Project Structure**

Your project has two parts:
- **Frontend**: Static HTML/CSS/JS files (can be deployed to Netlify)
- **Backend**: FastAPI server with database (needs a server platform)

## 🌐 **Option 1: Netlify (Frontend) + Render (Backend)**

### **Step 1: Deploy Backend to Render**

1. **Go to [Render.com](https://render.com)** and sign up
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name**: `ship-fuel-optimizer-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn apps:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: Leave empty (or `backend`)

5. **Add Environment Variables:**
   - `PORT`: `8000`

6. **Deploy** and wait for the build to complete
7. **Copy the URL** (e.g., `https://your-app.onrender.com`)

### **Step 2: Update Frontend API URL**

1. **Edit `frontend/script.js`**
2. **Change line 2:**
   ```javascript
   const API_BASE_URL = 'https://your-app.onrender.com'; // Your Render URL
   ```

### **Step 3: Deploy Frontend to Netlify**

1. **Go to [Netlify.com](https://netlify.com)** and sign up
2. **Drag and drop the `frontend` folder** to deploy
3. **Or connect your GitHub repository** and set:
   - **Build command**: Leave empty
   - **Publish directory**: `frontend`

4. **Your site will be live** at `https://your-site.netlify.app`

## 🌐 **Option 2: Netlify (Frontend) + Railway (Backend)**

### **Step 1: Deploy Backend to Railway**

1. **Go to [Railway.app](https://railway.app)** and sign up
2. **Create a new project** from GitHub
3. **Add a new service** → **GitHub Repo**
4. **Configure:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn apps:app --host 0.0.0.0 --port $PORT`

5. **Deploy** and copy the URL

### **Step 2: Deploy Frontend to Netlify**

Same as Option 1, Step 3, but update the API URL to your Railway URL.

## 🌐 **Option 3: Vercel (Frontend) + Vercel (Backend)**

### **Step 1: Deploy Backend to Vercel**

1. **Create `vercel.json` in the root:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "backend/apps.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "backend/apps.py"
       }
     ]
   }
   ```

2. **Deploy to Vercel** and copy the URL

### **Step 2: Deploy Frontend to Vercel**

1. **Deploy the `frontend` folder** to Vercel
2. **Update the API URL** in `script.js`

## 🔧 **Local Development**

For local development, use:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

## 📝 **Important Notes**

### **CORS Configuration**
Your backend already has CORS configured to allow all origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Database**
The `ports.db` file is included in the repository, so it will be available on deployment.

### **Environment Variables**
- `PORT`: Set by the hosting platform
- No additional environment variables needed

## 🚀 **Quick Deploy Commands**

### **Render (Backend)**
```bash
# Render will automatically detect and deploy
# Just push to GitHub and connect the repository
```

### **Netlify (Frontend)**
```bash
# Option 1: Drag and drop frontend folder
# Option 2: Connect GitHub and set publish directory to 'frontend'
```

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **CORS Errors**: Backend CORS is already configured
2. **Port Issues**: Use `$PORT` environment variable
3. **Database Not Found**: Ensure `ports.db` is in the backend folder
4. **API Connection**: Check the API_BASE_URL in `script.js`

### **Testing Deployment:**

1. **Test Backend**: Visit `https://your-backend-url.com/`
2. **Test Frontend**: Visit your Netlify/Vercel URL
3. **Test API**: Try a simple route like `London` → `Antwerp`

## 📞 **Support**

If you encounter issues:
1. Check the deployment platform logs
2. Verify the API_BASE_URL is correct
3. Ensure all files are in the correct folders
4. Test the backend API endpoints directly

Your Ship Fuel Optimizer will be live and accessible from anywhere! 🚢⚡ 