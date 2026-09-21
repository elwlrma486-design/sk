import json
import os
from pathlib import Path
import requests
import pandas as pd

API_KEY = os.environ.get("DART_API_KEY")
CORP_CODE = "00164779"
START_YEAR, END_YEAR = 2016, 2025
BASE = "https://opendart.fss.or.kr/api"
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

if not API_KEY:
    raise SystemExit("DART_API_KEY 환경변수가 필요합니다.")

def get_json(endpoint, params):
    r = requests.get(f"{BASE}/{endpoint}.json", params={"crtfc_key": API_KEY, **params}, timeout=60)
    r.raise_for_status()
    data = r.json()
    if str(data.get("status")) != "000":
        raise RuntimeError(f"{endpoint}: {data.get('status')} {data.get('message')}")
    return data

def main():
    rows = []
    for year in range(START_YEAR, END_YEAR + 1):
        data = get_json("fnlttSinglAcntAll", {
            "corp_code": CORP_CODE, "bsns_year": str(year),
            "reprt_code": "11011", "fs_div": "CFS"
        })
        (RAW / f"financials_{year}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        rows.extend(data.get("list", []))
        print(year, len(data.get("list", [])))
    pd.DataFrame(rows).to_csv(RAW / "financials_2016_2025_raw.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
