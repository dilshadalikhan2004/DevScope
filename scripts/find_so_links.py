import urllib.request
import re

def main():
    urls = [
        "https://insights.stackoverflow.com/survey",
        "https://survey.stackoverflow.co/",
        "https://insights.stackoverflow.com/survey/2024",
        "https://insights.stackoverflow.com/survey/2023"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    found_zips = set()
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
            matches = re.findall(r'href=["\'](https?://[^"\']+\.(?:zip|csv))["\']', html, re.IGNORECASE)
            for m in matches:
                found_zips.add(m)
            # also look for direct links in text
            matches_raw = re.findall(r'https?://[^\s"\'<>]+\.(?:zip|csv)', html, re.IGNORECASE)
            for m in matches_raw:
                found_zips.add(m)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    print("Found ZIP/CSV URLs:")
    for z in sorted(found_zips):
        print(" -", z)

if __name__ == "__main__":
    main()
