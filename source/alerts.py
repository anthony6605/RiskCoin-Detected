import pandas as pd

THRESHOLD = 0.01  # 1 cent deviation from peg

def check_alerts(processed_file="data/processed/stablecoin_metrics.csv"):
    df = pd.read_csv(processed_file)
    latest = df.tail(len(df["coin"].unique()))

    alerts = []
    for _, row in latest.iterrows():
        if abs(row["deviation_from_peg"]) > THRESHOLD:
            alerts.append(f"⚠️ {row['coin']} deviated from peg: ${row['price']:.4f}")

    if alerts:
        print("\n".join(alerts))
    else:
        print("✅ All stablecoins within safe range.")

if __name__ == "__main__":
    check_alerts()