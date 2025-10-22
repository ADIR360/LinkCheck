# Vercel Deployment Fix for link-check-seven.vercel.app

## Current Issue
The deployment at https://link-check-seven.vercel.app is showing 404 errors.

## Solution Steps

### 1. Update Vercel Project Settings
In your Vercel dashboard:
- Go to your project settings
- Set **Framework Preset** to "Other" or "Static Site"
- Set **Root Directory** to `frontend`
- Set **Build Command** to empty or `echo "No build needed"`
- Set **Output Directory** to `.` (current directory)

### 2. Environment Variables
Add these environment variables in Vercel:
```
VITE_API_URL=https://your-backend-domain.com
```

### 3. Redeploy
- Trigger a new deployment from the Vercel dashboard
- Or push a new commit to trigger automatic deployment

### 4. Alternative: Manual File Upload
If the above doesn't work:
1. Download the `frontend` folder from GitHub
2. Zip the contents of the frontend folder
3. In Vercel, go to "Deployments" → "Import Project"
4. Upload the zip file
5. Deploy

## Expected Result
After fixing, your site should be accessible at:
- https://link-check-seven.vercel.app
- All routes should work properly
- The Vue.js dashboard should load

## Backend Deployment
Don't forget to deploy your backend separately:
- Railway: https://railway.app
- Render: https://render.com
- Heroku: https://heroku.com

Then update the `VITE_API_URL` environment variable with your backend URL.
