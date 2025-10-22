# Click Tracker - Advanced Link Analytics

A production-ready web application for creating tracked links with comprehensive analytics.

## Features

- **Seamless Redirects**: No URL changes visible to users
- **Comprehensive Analytics**: IP, geolocation, device info, browser details
- **Modern Web Interface**: Vue.js frontend with real-time stats
- **Production Ready**: Gunicorn WSGI server, environment configuration
- **Multiple Geolocation Sources**: GeoIP2 database + IPInfo API fallback
- **Detailed Device Detection**: Browser, OS, device type, model, brand
- **Real-time Statistics**: Click counts, unique visitors, country breakdown

## Quick Start

### 1. Install Dependencies
```bash
cd click-tracker
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp config.env.example .env
# Edit .env with your settings
```

### 3. Run the Application
```bash
# Development
python backend/app.py

# Production
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

### 4. Access the Interface
Open `http://localhost:8000` in your browser.

## Configuration

### Environment Variables

- `BASE_URL`: Your domain (e.g., `https://tracker.yourdomain.com`)
- `IPINFO_TOKEN`: Free token from [ipinfo.io](https://ipinfo.io) for geolocation
- `GEOIP_DB_PATH`: Path to GeoIP2 database for more accurate geolocation
- `SECRET_KEY`: Random secret key for security
- `HOST`, `PORT`: Server binding settings

### Geolocation Setup

**Option 1: IPInfo (Free)**
1. Sign up at [ipinfo.io](https://ipinfo.io)
2. Get your free token
3. Set `IPINFO_TOKEN` in your `.env` file

**Option 2: GeoIP2 Database (More Accurate)**
1. Download from [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geoip-database)
2. Extract the `.mmdb` file
3. Set `GEOIP_DB_PATH` to the file path

## Data Collected

### Basic Information
- IP Address
- User Agent
- Referrer
- Timestamp
- Language preferences

### Geolocation Data
- Country, Region, City
- Postal Code
- Latitude/Longitude
- Timezone
- ISP/Organization

### Device Information
- Browser name and version
- Operating System and version
- Device type (mobile/tablet/desktop/bot)
- Device brand and model
- Screen resolution (if available)

### Additional Data
- Connection type
- Timezone
- Security headers
- Do Not Track preference

## API Endpoints

### Create Link
```bash
POST /api/links
{
  "url": "https://example.com",
  "title": "My Link",
  "code": "custom-code"
}
```

### List Links
```bash
GET /api/links
```

### Get Link Stats
```bash
GET /api/stats/{code}
```

### Health Check
```bash
GET /health
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "backend.app:app"]
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name tracker.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## File Structure

```
click-tracker/
├── backend/
│   └── app.py              # Main Flask application
├── frontend/
│   └── index.html          # Vue.js frontend
├── data/                   # Data storage
│   ├── links.json         # Link mappings
│   ├── clicks.csv         # Click logs
│   └── stats.json         # Aggregated statistics
├── requirements.txt        # Python dependencies
└── config.env.example     # Configuration template
```

## Security Notes

- All redirects are seamless (no visible URL changes)
- IP addresses are logged for analytics
- No personal data is collected beyond technical metadata
- Use HTTPS in production
- Set strong SECRET_KEY
- Consider rate limiting for production use

## Troubleshooting

### Common Issues

1. **SSL Certificate Errors**: Use `--trusted-host` flags with pip
2. **Permission Errors**: Ensure data directory is writable
3. **Geolocation Not Working**: Check IPINFO_TOKEN or GEOIP_DB_PATH
4. **Frontend Not Loading**: Ensure static files are served correctly

### Logs
Check application logs for detailed error information:
```bash
tail -f /var/log/click-tracker.log
```

## License

MIT License - Feel free to modify and use for your projects.
