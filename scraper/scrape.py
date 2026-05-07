from dotenv import load_dotenv
import requests
import os
import re

load_dotenv()

def fetch_html(url):
    headers = {
        "User-Agent": "OTT Player/1.7.4.1 (Linux;Android 16; en; htogzj)",
        "Host": "public.kliv.in",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def parse_channels(html):
    channels = []
    seen_urls = set()  # for deduplication

    lines = html.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Look for real EXTINF lines with a non-empty tvg-id
        if line.startswith("#EXTINF") and 'tvg-id="' in line:
            tvg_id_match = re.search(r'tvg-id="([^"]*)"', line)
            tvg_id = tvg_id_match.group(1) if tvg_id_match else ""

            # Skip junk channels with empty tvg-id
            if not tvg_id:
                i += 1
                continue

            extinf_line = line

            # Skip any #EXTVLCOPT lines
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("#"):
                j += 1

            # Next non-comment line should be the stream URL
            if j < len(lines):
                stream_url = lines[j].strip()

                # Only keep kliv.in URLs
                if "kliv.in" in stream_url and stream_url not in seen_urls:
                    seen_urls.add(stream_url)
                    channels.append((extinf_line, stream_url))

            i = j + 1
        else:
            i += 1

    return channels

def build_m3u(channels):
    lines = ["#EXTM3U8"]
    for extinf, url in channels:
        lines.append(extinf)
        lines.append(url)
    return "\n".join(lines)

def save_m3u(content):
    os.makedirs("output", exist_ok=True)
    with open("output/merged.m3u8", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {content.count('#EXTINF')} channels to output/merged.m3u8")

def scrape_epg():
    url = os.environ.get("EPG_SOURCE_URL")
    print(f"URL: {url}")
    print(f"Fetching from source...")
    html = fetch_html(url)
    print(f"Fetched {len(html)} characters")

    channels = parse_channels(html)
    print(f"Found {len(channels)} valid kliv.in channels")

    m3u = build_m3u(channels)
    save_m3u(m3u)

if __name__ == "__main__":
    scrape_epg()
