
#!/usr/bin/env python3

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
            if href.lower().split("?")[0].endswith(".png"):
                self.links.append(href)

def download_artwork():

    print("\nMAME Artwork Downloader")
    print("=======================")
    print("1. Add missing files")
    print("2. Update all files")
    print("0. Exit")

    choice = input("\nSelect an option: ").strip()

    if choice == "0":
        print("Exiting.")
        return

    if choice not in ("1", "2"):
        print("Invalid selection.")
        return

    update_all = choice == "2"

    print("\nReading Libretro directory...")

    req = urllib.request.Request(
        base,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = Parser()
    parser.feed(html)

    total = len(parser.links)
    downloaded = 0
    skipped = 0
    failed = 0

    print(f"Found {total} PNG images.\n")

    for i, link in enumerate(parser.links, 1):

        url = urljoin(base, link)
        filename = os.path.basename(unquote(link))

        if not filename:
            continue

        if os.path.exists(filename) and not update_all:
            skipped += 1
            print(f"[{i}/{total}] Skipping: {filename}")
            continue

        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()

            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("Downloaded file is not a valid PNG")

            with open(filename, "wb") as file:
                file.write(data)

            downloaded += 1
            print(f"[{i}/{total}] Downloaded: {filename}")

        except Exception as e:
            failed += 1
            print(f"[{i}/{total}] FAILED: {filename} - {e}")

    print("\n=======================")
    print("Download complete!")
    print(f"Total images: {total}")
    print(f"Downloaded:   {downloaded}")
    print(f"Skipped:      {skipped}")
    print(f"Failed:       {failed}")
    print("=======================\n")


if __name__ == "__main__":
    download_artwork()