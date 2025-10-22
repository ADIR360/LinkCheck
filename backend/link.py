#!/usr/bin/env python3
import argparse
import json
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LINKS_FILE = DATA_DIR / "links.json"

if DATA_DIR.exists() and not DATA_DIR.is_dir():
    DATA_DIR.unlink()  # Remove file if it exists
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


def generate_code(length: int = 7) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_link(url: str, code: str | None = None) -> str:
    links = load_links()
    if not code:
        code = generate_code()
        while code in links:
            code = generate_code()
    elif code in links:
        raise SystemExit("Code already exists. Choose another or omit --code.")

    links[code] = {"url": url}
    save_links(links)
    return code


def main():
    parser = argparse.ArgumentParser(description="Create tracked redirect links")
    parser.add_argument("url", help="Destination URL")
    parser.add_argument("--code", help="Custom short code", default=None)
    parser.add_argument(
        "--base", help="Base URL to your tracker server (e.g., https://x.y)", default="http://localhost:8000"
    )
    args = parser.parse_args()

    code = create_link(args.url, args.code)
    tracked = f"{args.base.rstrip('/')}/r/{code}"
    print(tracked)


if __name__ == "__main__":
    main()

