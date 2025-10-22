# Click Tracker Frontend

This is the frontend for the Click Tracker application - a modern Vue.js dashboard for managing tracked links and viewing analytics.

## Features

- 🎨 Modern Vue.js interface with real-time updates
- 📊 Comprehensive analytics dashboard
- 🔗 Link management and creation
- 📱 Responsive design for all devices
- ⚡ Fast and lightweight

## Deployment

### Vercel Deployment

1. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import this repository
   - Select the `frontend` folder as the root directory

2. **Configure Environment Variables:**
   - In Vercel dashboard, go to Settings > Environment Variables
   - Add `VITE_API_URL` with your backend URL (e.g., `https://your-backend.herokuapp.com`)

3. **Deploy:**
   - Vercel will automatically deploy on every push to main branch
   - Your frontend will be available at `https://your-project.vercel.app`

### Manual Deployment

```bash
# Clone the repository
git clone https://github.com/ADIR360/LinkCheck.git
cd LinkCheck/frontend

# Serve locally
python -m http.server 3000
```

## Configuration

The frontend automatically detects the environment:
- **Local development**: Uses `http://localhost:8000` for API calls
- **Production**: Uses the configured `VITE_API_URL` environment variable

## Backend Requirements

Make sure your backend is deployed and accessible. The frontend expects these API endpoints:

- `GET /api/links` - List all tracked links
- `POST /api/links` - Create a new tracked link
- `GET /api/stats/{code}` - Get statistics for a specific link

## Customization

To customize the API URL for different environments, update the `API_URL` constant in `index.html`:

```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://your-backend-domain.com';
```

## Support

For issues and questions, please refer to the main repository: [ADIR360/LinkCheck](https://github.com/ADIR360/LinkCheck)
