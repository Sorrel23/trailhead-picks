#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver...) with post URLs. Usage: indexnow.py _posts/FILE.md [...] | --all"""
import json, pathlib, re, sys, urllib.request
KEY = "21350eab6982ce9e60dc902902548eca"
BASE = "https://sorrel23.github.io/trailhead-picks"
posts = sorted(pathlib.Path("_posts").glob("*.md")) if sys.argv[1:] == ["--all"] else [pathlib.Path(p) for p in sys.argv[1:]]
urls = [f"{BASE}/{re.sub(r'^\d{4}-\d{2}-\d{2}-', '', p.stem)}/" for p in posts] + [f"{BASE}/"]
body = json.dumps({"host": "sorrel23.github.io", "key": KEY, "keyLocation": f"{BASE}/{KEY}.txt", "urlList": urls}).encode()
r = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(r, timeout=30) as resp: print("IndexNow", resp.status, urls)
except urllib.error.HTTPError as e: print("IndexNow error", e.code, e.read()[:300]); 
