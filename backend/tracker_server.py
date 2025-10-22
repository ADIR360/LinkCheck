#!/usr/bin/env python3
import os
import json
import csv
import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask, request, redirect, abort, jsonify

try:
    # Prefer ua_parser for robust parsing
    from ua_parser import user_agent_parser
except Exception:  # pragma: no cover - fallback if not installed
    user_agent_parser = None

try:
    import requests  # optional for geolocation
except Exception:  # pragma: no cover
    requests = None


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LINKS_FILE = DATA_DIR / "links.json"
CLICKS_FILE = DATA_DIR / "clicks.csv"

if DATA_DIR.exists() and not DATA_DIR.is_dir():
    DATA_DIR.unlink()  # Remove file if it exists
DATA_DIR.mkdir(exist_ok=True)


def _load_links() -> Dict[str, Dict[str, Any]]:
    if not LINKS_FILE.exists():
        return {}
    try:
        return json.loads(LINKS_FILE.read_text())
    except Exception:
        return {}


def _save_links(data: Dict[str, Dict[str, Any]]) -> None:
    LINKS_FILE.write_text(json.dumps(data, indent=2))


def parse_user_agent(ua_string: str) -> Dict[str, Optional[str]]:
    if not ua_string:
        return {"browser": None, "os": None, "device": None}

    if user_agent_parser is None:
        return {"browser": None, "os": None, "device": None}

    parsed = user_agent_parser.Parse(ua_string)
    browser = parsed.get("user_agent", {})
    os_info = parsed.get("os", {})
    device = parsed.get("device", {})

    browser_str = " ".join(filter(None, [browser.get("family"), browser.get("major")])) or None
    os_str = " ".join(filter(None, [os_info.get("family"), os_info.get("major")])) or None
    device_str = ", ".join(
        [v for v in [device.get("brand"), device.get("model"), device.get("family")] if v]
    ) or None

    return {"browser": browser_str, "os": os_str, "device": device_str}


def geo_lookup(ip: str) -> Dict[str, Optional[str]]:
    # Approximate, city-level at best. Requires external API and token; gracefully degrade.
    token = os.getenv("IPINFO_TOKEN")
    if not token or not requests or not ip:
        return {}
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}", params={"token": token}, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "ip_country": data.get("country"),
                "ip_region": data.get("region"),
                "ip_city": data.get("city"),
                "ip_loc": data.get("loc"),
                "ip_org": data.get("org"),
            }
    except Exception:
        pass
    return {}


def append_click_row(row: Dict[str, Any]) -> None:
    exists = CLICKS_FILE.exists()
    with CLICKS_FILE.open("a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "code",
                "target_url",
                "ip",
                "ip_country",
                "ip_region",
                "ip_city",
                "ip_loc",
                "ip_org",
                "browser",
                "os",
                "device",
                "user_agent",
                "referer",
                "accept_language",
            ],
        )
        if not exists:
            writer.writeheader()
        writer.writerow(row)


app = Flask(__name__)


@app.get("/health")
def health() -> Any:
    return {"status": "ok"}


@app.get("/r/<code>")
def redirect_with_logging(code: str):
    links = _load_links()
    entry = links.get(code)
    if not entry:
        abort(404, description="Unknown code")

    target_url = entry.get("url")
    if not target_url:
        abort(500, description="Invalid link mapping")

    # Gather request metadata
    ua = request.headers.get("User-Agent", "")
    parsed_ua = parse_user_agent(ua)
    referer = request.headers.get("Referer")
    accept_language = request.headers.get("Accept-Language")

    # Best-effort IP
    # X-Forwarded-For may contain multiple IPs; first is client
    xff = request.headers.get("X-Forwarded-For")
    ip = (xff.split(",")[0].strip() if xff else request.remote_addr) or ""
    geo = geo_lookup(ip)

    row = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "code": code,
        "target_url": target_url,
        "ip": ip,
        "ip_country": geo.get("ip_country"),
        "ip_region": geo.get("ip_region"),
        "ip_city": geo.get("ip_city"),
        "ip_loc": geo.get("ip_loc"),
        "ip_org": geo.get("ip_org"),
        "browser": parsed_ua.get("browser"),
        "os": parsed_ua.get("os"),
        "device": parsed_ua.get("device"),
        "user_agent": ua,
        "referer": referer,
        "accept_language": accept_language,
    }

    try:
        append_click_row(row)
    except Exception:
        # Do not block redirect on logging errors
        pass

    return redirect(target_url, code=302)


@app.post("/links")
def create_link():
    payload = request.get_json(silent=True) or {}
    url = payload.get("url")
    code = payload.get("code")
    if not url:
        abort(400, description="Missing url")
    if not code:
        abort(400, description="Missing code")

    links = _load_links()
    if code in links:
        abort(409, description="Code already exists")
    links[code] = {"url": url, "created_at": datetime.datetime.utcnow().isoformat() + "Z"}
    _save_links(links)
    return jsonify({"code": code, "url": url, "redirect": f"/r/{code}"}), 201


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()


