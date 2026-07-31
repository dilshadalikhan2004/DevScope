"""
DevScope - Real Stack Overflow Survey Ingestion Script
Downloads authentic Stack Overflow survey datasets (2021-2024) from the
official StackExchange repository into data/raw/.
"""

import sys
import urllib.request
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import RAW_SURVEY_PATHS, DATA_DIR
from etl.logger import get_logger

logger = get_logger(__name__)

OFFICIAL_SO_URLS = {
    2024: "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive/2024/results.csv",
    2023: "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive/2023/results.csv",
    2022: "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive/2022/results.csv",
    2021: "https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive/2021/results.csv"
}

def download_official_surveys():
    """Downloads real Stack Overflow survey datasets directly into data/raw/."""
    raw_dir = DATA_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for year, url in OFFICIAL_SO_URLS.items():
        target_path = RAW_SURVEY_PATHS[year]
        logger.info(f"Downloading official Stack Overflow {year} Developer Survey dataset from {url}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp, open(target_path, 'wb') as out_file:
                content = resp.read()
                out_file.write(content)
            logger.info(f"Successfully saved official {year} Stack Overflow survey ({len(content):,} bytes) to {target_path.name}")
        except Exception as e:
            logger.error(f"Failed to download official {year} dataset from {url}: {e}")

if __name__ == "__main__":
    download_official_surveys()
