from pathlib import Path
import numpy as np
import pandas as pd

STATIONS = ["LKO1", "DEL2", "HYD3", "BLR4", "CCU5", "BOM6"]
CARRIERS = ["RapidX", "BlueRoute", "SwiftLog", "PrimeMove"]
CAUSES = ["No exception", "Vehicle breakdown", "Capacity constraint", "Weather", "Address issue", "Late dispatch", "Driver unavailable"]

def generate_shipments(n=1500, seed=10418348):
    rng = np.random.default_rng(seed)
    created = pd.Timestamp.now().floor("h") - pd.to_timedelta(rng.integers(0, 24 * 14, n), unit="h")
    promised = created + pd.to_timedelta(rng.integers(8, 60, n), unit="h")
    station = rng.choice(STATIONS, n)
    carrier = rng.choice(CARRIERS, n, p=[.30, .25, .25, .20])
    exception = rng.random(n) < .22
    cause = np.where(exception, rng.choice(CAUSES[1:], n, p=[.12,.22,.10,.18,.25,.13]), CAUSES[0])
    delay = np.where(exception, rng.gamma(2.2, 4.5, n), rng.normal(-2, 2.2, n))
    actual = promised + pd.to_timedelta(delay, unit="h")
    status = np.where(actual <= pd.Timestamp.now(), "Delivered", np.where(exception, "Exception", "In Transit"))
    opened = np.where(exception, created + pd.to_timedelta(rng.integers(2, 18, n), unit="h"), pd.NaT)
    age = np.where(exception, np.maximum(0, (pd.Timestamp.now() - pd.to_datetime(opened)).total_seconds() / 3600), 0)
    customer_contacts = np.where(exception, rng.poisson(1.4, n), 0)
    df = pd.DataFrame({
        "shipment_id": [f"TR-{i+1:06d}" for i in range(n)],
        "station": station, "carrier": carrier, "created_at": created,
        "promised_delivery": promised, "actual_or_expected_delivery": actual,
        "status": status, "exception_reason": cause,
        "exception_opened_at": opened, "exception_age_hours": age.round(1),
        "customer_contacts": customer_contacts,
        "packages": rng.integers(1, 15, n)
    })
    return df

if __name__ == "__main__":
    path = Path("data")
    path.mkdir(exist_ok=True)
    generate_shipments().to_csv(path / "transportation_events.csv", index=False)
    print("Created data/transportation_events.csv")
