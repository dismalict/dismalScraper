import requests
import json
import csv
from datetime import datetime

# ==== CONFIG ====
COMPANY_ID = "78802"
DASHBOARD_ID = "956825"

# Put your welder asset IDs here
ASSET_IDS = [
    "42998400",   # Example welder
    # "another_id",
    # "another_id"
]

# Date range (YYYYMMDD)
DATE_FROM = "20250828"
DATE_TO   = "20250828"

# Copy cookies from your browser (DevTools → Application → Cookies)
COOKIES = {
    "SESSIONID": "your_session_cookie_here"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}
# =================


def fetch_data(asset_id):
    """Fetch all 3 API calls for a given asset_id"""

    base = f"https://checkpoint.lincolnelectric.com/api/reports"

    urls = {
        "dashboard": (
            f"{base}/dashboard/{COMPANY_ID}/{DASHBOARD_ID}"
            f"?asset_id={asset_id}&asset_type=EQUIPMENTROLE"
            f"&shift_id=allshifts&from={DATE_FROM}&to={DATE_TO}"
            f"&aggregation_type=PRODUCTIONDATA&display_unit=IMPERIAL"
        ),
        "activity": (
            f"{base}/dashboard/activity/{COMPANY_ID}/{DASHBOARD_ID}"
            f"?asset_id={asset_id}&asset_type=EQUIPMENTROLE"
            f"&shift_id=allshifts&from={DATE_FROM}&to={DATE_TO}"
            f"&aggregation_type=PRODUCTIONDATA"
        ),
        "reportRange": (
            f"{base}/reportRange/{COMPANY_ID}/{DASHBOARD_ID}"
            f"?shift_id=allshifts&from={DATE_FROM}&to={DATE_TO}"
            f"&aggregation_type=PRODUCTIONDATA"
        ),
    }

    results = {}
    for key, url in urls.items():
        r = requests.get(url, headers=HEADERS, cookies=COOKIES)
        if r.status_code == 200:
            try:
                results[key] = r.json()
            except:
                results[key] = {"error": "Invalid JSON", "raw": r.text}
        else:
            results[key] = {"error": f"HTTP {r.status_code}"}
    return results


def save_to_files(all_data):
    """Save JSON and CSV outputs"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save raw JSON
    with open(f"checkpoint_raw_{timestamp}.json", "w") as f:
        json.dump(all_data, f, indent=2)

    # Flatten into CSV (basic)
    with open(f"checkpoint_data_{timestamp}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["asset_id", "endpoint", "key", "value"])

        for asset_id, endpoints in all_data.items():
            for endpoint, data in endpoints.items():
                if isinstance(data, dict):
                    for k, v in data.items():
                        writer.writerow([asset_id, endpoint, k, v])
                else:
                    writer.writerow([asset_id, endpoint, "raw", str(data)])


def main():
    all_data = {}
    for asset_id in ASSET_IDS:
        print(f"Fetching data for asset {asset_id}...")
        all_data[asset_id] = fetch_data(asset_id)

    save_to_files(all_data)
    print("Done. Data saved to JSON + CSV.")


if __name__ == "__main__":
    main()
