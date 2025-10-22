# 🚀 Click Tracker - Complete Deployment Guide

## 📋 Overview

Your Click Tracker project has been successfully pushed to GitHub at [ADIR360/LinkCheck](https://github.com/ADIR360/LinkCheck.git). This guide will help you deploy both the backend and frontend to production.

## 🎯 Deployment Options

### Option 1: Full Stack Deployment (Recommended)

#### Backend Deployment (Railway/Render/Heroku)

1. **Railway (Recommended - Free tier available)**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account
   - Select the `LinkCheck` repository
   - Set root directory to `click-tracker`
   - Add environment variables:
     ```
     BASE_URL=https://your-app-name.railway.app
     IPINFO_TOKEN=your_ipinfo_token_here
     PORT=8000
     ```
   - Deploy automatically

2. **Render (Alternative)**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python backend/app.py`
   - Add environment variables as above

#### Frontend Deployment (Vercel)

1. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import from GitHub: `ADIR360/LinkCheck`
   - Set root directory to `frontend`
   - Add environment variable:
     ```
     VITE_API_URL=https://your-backend-domain.com
     ```
   - Deploy

### Option 2: Separate Deployments

#### Backend Only
Deploy just the backend to any Python hosting service and use the API directly.

#### Frontend Only
Deploy the frontend to Vercel and configure it to point to your existing backend.

## 🔧 Configuration

### Backend Environment Variables
```bash
BASE_URL=https://your-domain.com          # Your production domain
IPINFO_TOKEN=your_token_here              # Optional: for geolocation
PORT=8000                                 # Port (usually auto-set by host)
SECRET_KEY=your_secret_key_here           # Random secret key
```

### Frontend Environment Variables
```bash
VITE_API_URL=https://your-backend.com     # Your backend API URL
```

## 📱 Quick Start Commands

### Local Development
```bash
# Clone the repository
git clone https://github.com/ADIR360/LinkCheck.git
cd LinkCheck/click-tracker

# Start the application
./start.sh
```

### Production Deployment
```bash
# Backend (example with Railway)
railway login
railway link
railway up

# Frontend (example with Vercel)
vercel login
vercel --prod
```

## 🌐 Access Your Application

Once deployed:
- **Backend API**: `https://your-backend-domain.com/api/links`
- **Frontend Dashboard**: `https://your-frontend-domain.vercel.app`
- **Tracked Links**: `https://your-backend-domain.com/r/{code}`

## 📊 Features Available

✅ **Seamless Redirects** - No visible URL changes  
✅ **Comprehensive Analytics** - IP, device, browser, location data  
✅ **Modern Dashboard** - Vue.js interface with real-time stats  
✅ **CLI Tools** - Command-line link management  
✅ **Production Ready** - Proper error handling and logging  

## 🔗 Example Usage

Create a tracked link:
```bash
curl -X POST https://your-backend.com/api/links \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com","title":"GitHub","code":"github"}'
```

Result: `https://your-backend.com/r/github`

## 📞 Support

- **GitHub Repository**: [ADIR360/LinkCheck](https://github.com/ADIR360/LinkCheck)
- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: Check the README.md files in each directory

## 🎉 Success!

Your Click Tracker is now live and ready to track links with comprehensive analytics!
