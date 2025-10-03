import json
import os
import pandas as pd
from datetime import datetime

def transform_data(raw_file):
    with open(raw_file, "r") as f:
        data = json.load(f)

    records = []
    for coin, info in data.items():
        price = info.get("usd")
        change = info.get("usd_24h_change", 0)
        deviation = price - 1.0
        records.append({
            "coin": coin,
            "price": price,
            "deviation_from_peg": deviation,
            "24h_change": change,
            "timestamp": datetime.utcnow().isoformat()
        })

    df = pd.DataFrame(records)

    os.makedirs("data/processed", exist_ok=True)
    out_file = "data/processed/stablecoin_metrics.csv"
    if not os.path.exists(out_file):
        df.to_csv(out_file, index=False)
    else:
        df.to_csv(out_file, mode="a", header=False, index=False)

    print(f"✅ Transformed data saved to {out_file}")
    return df

if __name__ == "__main__":
    # Use the latest file from data/raw
    raw_files = sorted(os.listdir("data/raw"))
    latest_file = os.path.join("data/raw", raw_files[-1])
    transform_data(latest_file)