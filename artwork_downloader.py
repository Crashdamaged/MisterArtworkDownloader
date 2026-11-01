
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, unquote
import os

base = "https://thumbnails.libretro.com/MAME/Named_Titles/"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.lower().endswith(".png"):
                self.links.append(href)

req = urllib.request.Request(
    base,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req) as response:
    html = response.read().decode("utf-8", errors="replace")

parser = Parser()
parser.feed(html)

print(f"Found {len(parser.links)} PNG images")

for i, link in enumerate(parser.links, 1):
    url = urljoin(base, link)
    filename = os.path.basename(unquote(link))

    if os.path.exists(filename):
        print(f"{i}/{len(parser.links)} Skipping: {filename}")
        continue

    try:
        urllib.request.urlretrieve(url, filename)
        print(f"{i}/{len(parser.links)} Downloaded: {filename}")
    except Exception as e:
        print(f"Failed: {filename} - {e}")

print("Download complete")