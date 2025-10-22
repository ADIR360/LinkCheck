#!/usr/bin/env python3
import argparse
import json
import secrets
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LINKS_FILE = DATA_DIR / "links.json"

DATA_DIR.mkdir(exist_ok=True)

def load_links():
    if not LINKS_FILE.exists():
        return {}
    try:
        return json.loads(LINKS_FILE.read_text())
    except Exception:
        return {}

def save_links(data):
    LINKS_FILE.write_text(json.dumps(data, indent=2))

def generate_code(length: int = 8) -> str:
    return secrets.token_urlsafe(length)

def create_link(url: str, code: str = None, title: str = None, base_url: str = "http://localhost:8000") -> str:
    """Create a tracked link via API or local storage"""
    
    # Try API first
    try:
        response = requests.post(f"{base_url}/api/links", json={
            "url": url,
            "title": title,
            "code": code
        }, timeout=5)
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Link created successfully!")
            print(f"📊 Dashboard: {base_url}")
            print(f"🔗 Tracked URL: {data['tracked_url']}")
            return data['tracked_url']
        else:
            print(f"❌ API Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  API unavailable ({e}), using local storage")
    
    # Fallback to local storage
    links = load_links()
    if not code:
        code = generate_code()
        while code in links:
            code = generate_code()
    elif code in links:
        raise SystemExit("❌ Code already exists. Choose another or omit --code.")
    
    links[code] = {
        "url": url,
        "title": title or url,
        "created_at": "2024-01-01T00:00:00Z"  # Placeholder
    }
    save_links(links)
    
    tracked_url = f"{base_url}/r/{code}"
    print(f"✅ Link created locally!")
    print(f"🔗 Tracked URL: {tracked_url}")
    print(f"⚠️  Note: Start the server to make this link active")
    return tracked_url

def list_links(base_url: str = "http://localhost:8000"):
    """List all tracked links"""
    try:
        response = requests.get(f"{base_url}/api/links", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total Links: {len(data['links'])}")
            print(f"👥 Total Clicks: {data['stats']['total_clicks']}")
            print(f"🌍 Unique Visitors: {data['stats']['unique_ips']}")
            print()
            
            for link in data['links']:
                print(f"🔗 {link['title']}")
                print(f"   Original: {link['url']}")
                print(f"   Tracked:  {link['tracked_url']}")
                print(f"   Clicks:   {link['clicks']}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running with: python backend/app.py")

def main():
    parser = argparse.ArgumentParser(description="Click Tracker CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a tracked link')
    create_parser.add_argument('url', help='Destination URL')
    create_parser.add_argument('--title', help='Link title')
    create_parser.add_argument('--code', help='Custom short code')
    create_parser.add_argument('--base', default='http://localhost:8000', help='Base URL')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all tracked links')
    list_parser.add_argument('--base', default='http://localhost:8000', help='Base URL')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_link(args.url, args.code, args.title, args.base)
    elif args.command == 'list':
        list_links(args.base)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
