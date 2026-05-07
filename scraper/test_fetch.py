from dotenv import load_dotenv
import requests
import os

load_dotenv()

def scrape_epg():
    url = os.environ.get("EPG_SOURCE_URL")
    headers = {
        "User-Agent": "OTT Player/1.7.4.1 (Linux;Android 16; en; htogzj)",
        "Host": "public.kliv.in",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response length: {len(response.text)} characters")
        print(f"First 700 chars:\n{response.text[:700]}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_epg()
