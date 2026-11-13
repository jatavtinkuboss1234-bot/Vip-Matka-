import json
import re
import urllib.request
from datetime import datetime

MARKET_NAMES = {
    "laxmi": "LAXMI MORNING",
    "kalyan": "KALYAN",
    "sridevi_night": "SRIDEVI NIGHT",
    "supreme_night": "SUPREME NIGHT",
    "milan_day": "MILAN DAY",
    "rajdhani_night": "RAJDHANI NIGHT"
}

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')

def main():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except Exception:
        data = {}

    try:
        html = fetch_html("https://sattamatka.org/")
        clean_text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html))

        for key, title in MARKET_NAMES.items():
            match = re.search(rf"{title}.*?(\d{{3}}\s*-\s*\d{{2}}\s*-\s*\d{{3}})", clean_text, re.IGNORECASE)
            if match:
                latest_res = match.group(1).strip()
                jodi = latest_res.split('-')[1].strip()
                if key not in data:
                    data[key] = {"name": title, "latest": latest_res, "history": [jodi]}
                else:
                    data[key]["latest"] = latest_res
                    if not data[key]["history"] or data[key]["history"][-1] != jodi:
                        data[key]["history"].append(jodi)
                        data[key]["history"] = data[key]["history"][-60:]
    except Exception as e:
        print("Sync warning:", e)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Updated at", datetime.now())

if __name__ == "__main__":
    main()
