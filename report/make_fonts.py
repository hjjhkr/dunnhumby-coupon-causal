"""Download the report's Google Fonts once and write them into report/fonts.css as base64 data,
so the standalone report needs no network to show the right typefaces.

Only the Latin subset is kept. All three families are under the SIL Open Font License, which allows embedding.
Run: python report/make_fonts.py
"""
import base64
import pathlib
import re
import urllib.request

URL = ("https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600;8..60,700"
       "&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
        return r.read()


css = get(URL).decode("utf-8")
blocks = re.findall(r"/\* ([a-z\-]+) \*/\s*(@font-face \{.*?\})", css, flags=re.S)
out, seen = [], {}
for subset, block in blocks:
    if subset != "latin":
        continue
    url = re.search(r"url\((https://[^)]+)\)", block).group(1)
    if url not in seen:
        seen[url] = "data:font/woff2;base64," + base64.b64encode(get(url)).decode()
    out.append(block.replace(url, seen[url]))

path = pathlib.Path(__file__).with_name("fonts.css")
path.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"{len(out)} @font-face rules, {len(seen)} font files, {path.stat().st_size / 1024:.0f} KB -> {path}")
