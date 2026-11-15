#!/usr/bin/env python3
"""Create a Pinterest pin (official API v5) for each post given. Run by GitHub Actions.
Env: PINTEREST_BOARD_ID, and either PINTEREST_TOKEN or (PINTEREST_APP_ID, PINTEREST_APP_SECRET, PINTEREST_REFRESH_TOKEN).
Usage: post_pin.py _posts/FILE.md [...]"""
import base64, json, os, pathlib, re, subprocess, sys, tempfile, urllib.request
API = "https://api.pinterest.com/v5"
def req(url, data=None, headers=None, form=False):
    body = (data if form else json.dumps(data).encode()) if data is not None else None
    r = urllib.request.Request(url, data=body, headers=headers or {}, method="POST" if body else "GET")
    with urllib.request.urlopen(r, timeout=60) as resp: return json.load(resp)
def token():
    rt = os.environ.get("PINTEREST_REFRESH_TOKEN")
    if rt:
        basic = base64.b64encode(f'{os.environ["PINTEREST_APP_ID"]}:{os.environ["PINTEREST_APP_SECRET"]}'.encode()).decode()
        form = f"grant_type=refresh_token&refresh_token={rt}".encode()
        return req(f"{API}/oauth/token", form, {"Authorization": f"Basic {basic}",
                   "Content-Type": "application/x-www-form-urlencoded"}, form=True)["access_token"]
    return os.environ["PINTEREST_TOKEN"]
def cfg(key):
    m = re.search(rf'^{key}:\s*"?([^"#\n]*)"?', pathlib.Path("_config.yml").read_text(), re.M)
    return (m.group(1).strip() if m else "").rstrip("/")
def fm(t, k):
    m = re.search(rf'^{k}:\s*"?(.*?)"?\s*$', t, re.M); return m.group(1) if m else ""
def main(posts):
    if not os.environ.get("PINTEREST_BOARD_ID") or not (os.environ.get("PINTEREST_TOKEN") or os.environ.get("PINTEREST_REFRESH_TOKEN")):
        print("Pinterest secrets not set; skipping pins."); return
    site = cfg("url") + cfg("baseurl")
    tok = token()
    for p in posts:
        t = pathlib.Path(p).read_text()
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", pathlib.Path(p).stem)
        png = tempfile.mktemp(suffix=".png")
        subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "make_pin.py"), p, png], check=True)
        desc = f'{fm(t, "description")} Full list + links on Trailhead Picks. (Affiliate links: we may earn a commission.)'
        payload = {"board_id": os.environ["PINTEREST_BOARD_ID"], "title": fm(t, "pin_title")[:100],
                   "description": desc[:500], "link": f"{site}/{slug}/", "alt_text": fm(t, "pin_title")[:500],
                   "media_source": {"source_type": "image_base64", "content_type": "image/png",
                                    "data": base64.b64encode(open(png, "rb").read()).decode()}}
        r = req(f"{API}/pins", payload, {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        print(f"Pinned {p} -> pin {r.get('id')} linking {payload['link']}")
if __name__ == "__main__":
    main(sys.argv[1:])
