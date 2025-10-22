#!/usr/bin/env python3
import os
import json
import csv
import datetime
import secrets
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, request, redirect, abort, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LINKS_FILE = DATA_DIR / "links.json"
CLICKS_FILE = DATA_DIR / "clicks.csv"

DATA_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:8000')

def load_links():
    if not LINKS_FILE.exists():
        return {}
    try:
        return json.loads(LINKS_FILE.read_text())
    except Exception:
        return {}

def save_links(data):
    LINKS_FILE.write_text(json.dumps(data, indent=2))

def log_click(code, target_url, ip, ua):
    click_data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "code": code,
        "target_url": target_url,
        "ip": ip,
        "user_agent": ua
    }
    
    exists = CLICKS_FILE.exists()
    fieldnames = ["timestamp", "code", "target_url", "ip", "user_agent"]
    
    try:
        with CLICKS_FILE.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not exists:
                writer.writeheader()
            writer.writerow(click_data)
    except Exception as e:
        print(f"Failed to log click: {e}")

@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception:
        return "<h1>Click Tracker</h1><p>API is working! <a href='/api/links'>View Links</a></p>"

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/links', methods=['GET'])
def list_links():
    links = load_links()
    
    click_counts = {}
    if CLICKS_FILE.exists():
        try:
            with CLICKS_FILE.open('r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    code = row['code']
                    click_counts[code] = click_counts.get(code, 0) + 1
        except Exception:
            pass
    
    result = []
    for code, data in links.items():
        result.append({
            "code": code,
            "url": data["url"],
            "title": data.get("title", data["url"]),
            "tracked_url": f"{app.config['BASE_URL']}/r/{code}",
            "created_at": data.get("created_at", "Unknown"),
            "clicks": click_counts.get(code, 0)
        })
    
    return jsonify({
        "links": result,
        "stats": {
            "total_clicks": sum(click_counts.values()),
            "unique_ips": 0,
            "countries": {},
            "devices": {}
        }
    })

@app.route('/api/links', methods=['POST'])
def create_link():
    payload = request.get_json(silent=True) or {}
    url = payload.get('url', '').strip()
    code = payload.get('code', '').strip()
    title = payload.get('title', '').strip()
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if not code:
        code = secrets.token_urlsafe(8)
        links = load_links()
        while code in links:
            code = secrets.token_urlsafe(8)
    
    links = load_links()
    if code in links:
        return jsonify({"error": "Code already exists"}), 409
    
    links[code] = {
        "url": url,
        "title": title or url,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    save_links(links)
    
    tracked_url = f"{app.config['BASE_URL']}/r/{code}"
    return jsonify({
        "code": code,
        "url": url,
        "title": title or url,
        "tracked_url": tracked_url,
        "created_at": links[code]["created_at"]
    }), 201

@app.route('/api/stats/<code>')
def get_stats(code):
    links = load_links()
    if code not in links:
        return jsonify({"error": "Link not found"}), 404
    
    clicks = []
    if CLICKS_FILE.exists():
        try:
            with CLICKS_FILE.open('r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['code'] == code:
                        clicks.append(row)
        except Exception:
            pass
    
    return jsonify({
        "code": code,
        "url": links[code]["url"],
        "title": links[code].get("title", links[code]["url"]),
        "total_clicks": len(clicks),
        "clicks": clicks[-50:]
    })

@app.route('/r/<code>')
def redirect_link(code):
    links = load_links()
    entry = links.get(code)
    if not entry:
        abort(404)
    
    target_url = entry.get("url")
    if not target_url:
        abort(500)
    
    ip = request.remote_addr or ""
    ua = request.headers.get('User-Agent', '')
    
    log_click(code, target_url, ip, ua)
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Redirecting...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
            .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 20px auto; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <h2>Redirecting...</h2>
        <div class="spinner"></div>
        <p>You are being redirected to your destination.</p>
        <script>
            window.location.replace('{target_url}');
        </script>
    </body>
    </html>
    ''', 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"🚀 Starting Click Tracker on {host}:{port}")
    print(f"📊 Dashboard: http://{host}:{port}")
    print(f"🔗 API: http://{host}:{port}/api/links")
    
    app.run(host=host, port=port, debug=False)