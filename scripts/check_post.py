#!/usr/bin/env python3
"""Validate posts before publishing. Usage: check_post.py _posts/FILE.md [...]  (exit 1 on any error)"""
import re, sys, pathlib
REQ = ["layout", "title", "date", "description", "pin_title", "pin_text"]
BANNED = [r"\$\s?\d", r"\b\d(\.\d)?\s?(out of 5|stars?)\b", r"\bwe tested\b", r"\bI tested\b", r"\bin our testing\b",
          r"\bour testers\b", r"\bhands-on\b", r"\bI('ve| have) (used|owned)\b", r"\bdeal ends\b", r"\blowest price\b"]
def check(path):
    errs = []
    t = pathlib.Path(path).read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not m: return [f"{path}: missing front matter"]
    fm, body = m.groups()
    for k in REQ:
        if not re.search(rf"^{k}:\s*\S", fm, re.M): errs.append(f"missing front matter '{k}'")
    if not re.match(r"_posts/\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$", str(path).split("site/")[-1].lstrip("./")) and "/_posts/" not in str(path):
        errs.append("filename must be _posts/YYYY-MM-DD-slug.md")
    links = re.findall(r"{%\s*include amzn\.html (.*?)%}", body)
    if len(links) < 3: errs.append(f"only {len(links)} Amazon links (need >= 3)")
    for l in links:
        a = re.search(r'asin="([^"]*)"', l)
        if a and not re.fullmatch(r"B0[0-9A-Z]{8}|\d{9}[\dX]", a.group(1)): errs.append(f"bad ASIN {a.group(1)}")
        if not a and 'q="' not in l: errs.append(f"link needs asin= or q=: {l}")
    if re.search(r"amazon\.com/[^ )\"]*", body): errs.append("raw amazon.com URL in body; use the amzn.html include so the tag is applied")
    if re.search(r"amzn\.to|bit\.ly", body): errs.append("shortened link found")
    for b in BANNED:
        if re.search(b, body, re.I): errs.append(f"banned pattern /{b}/ (no prices, star ratings, or fake hands-on claims)")
    words = len(re.sub(r"{%.*?%}|<[^>]+>", " ", body).split())
    if words < 450: errs.append(f"only {words} words (need >= 450 of original commentary)")
    return [f"{path}: {e}" for e in errs]
if __name__ == "__main__":
    allerr = [e for p in sys.argv[1:] for e in check(p)]
    print("\n".join(allerr) or "OK")
    sys.exit(1 if allerr else 0)
