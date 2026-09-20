import pandas as pd

CRITICAL_REASONS = {"Vehicle breakdown", "Capacity constraint", "Driver unavailable"}
ACTION_MAP = {
    "Vehicle breakdown": "Confirm rescue vehicle and transfer packages",
    "Capacity constraint": "Rebalance volume or request additional capacity",
    "Weather": "Validate safe route and communicate revised ETA",
    "Address issue": "Trigger customer/address verification workflow",
    "Late dispatch": "Contact station and confirm departure plan",
    "Driver unavailable": "Request replacement driver and escalate carrier",
}

def enrich_cases(df, sla_hours=4):
    out = df.copy()
    out["promised_delivery"] = pd.to_datetime(out["promised_delivery"])
    out["actual_or_expected_delivery"] = pd.to_datetime(out["actual_or_expected_delivery"])
    out["late"] = out["actual_or_expected_delivery"] > out["promised_delivery"]
    out["open_exception"] = out["status"].eq("Exception")
    out["sla_breached"] = out["open_exception"] & (out["exception_age_hours"] > sla_hours)
    out["severity_score"] = (
        out["open_exception"].astype(int) * 30
        + out["sla_breached"].astype(int) * 35
        + out["exception_reason"].isin(CRITICAL_REASONS).astype(int) * 20
        + out["customer_contacts"].clip(0, 3) * 5
    )
    out["priority"] = pd.cut(out["severity_score"], [-1, 29, 59, 79, 1000], labels=["Normal", "Medium", "High", "Critical"])
    out["recommended_action"] = out["exception_reason"].map(ACTION_MAP).fillna("Monitor shipment")
    return out

def network_kpis(df):
    total = len(df)
    delivered = df[df.status.eq("Delivered")]
    open_cases = int(df.open_exception.sum())
    within_sla = int((df.open_exception & ~df.sla_breached).sum())
    return {
        "shipments": total,
        "on_time_rate": 1 - df.late.mean() if total else 0,
        "open_exceptions": open_cases,
        "critical_cases": int(df.priority.eq("Critical").sum()),
        "sla_compliance": within_sla / open_cases if open_cases else 1,
        "delivered": len(delivered),
    }

def exception_queue(df):
    cols = ["shipment_id", "station", "carrier", "priority", "exception_reason", "exception_age_hours", "customer_contacts", "recommended_action"]
    return df[df.open_exception].sort_values(["severity_score", "exception_age_hours"], ascending=False)[cols]

def stakeholder_update(df):
    kpi = network_kpis(df)
    top_reason = df.loc[df.open_exception, "exception_reason"].value_counts()
    top_station = df.loc[df.open_exception, "station"].value_counts()
    reason = top_reason.index[0] if not top_reason.empty else "None"
    station = top_station.index[0] if not top_station.empty else "None"
    return (
        f"Network update: {kpi['open_exceptions']} open transportation exceptions; "
        f"{kpi['critical_cases']} critical; SLA compliance {kpi['sla_compliance']:.1%}. "
        f"Highest exception concentration is at {station}; leading cause is {reason}. "
        "Critical cases are prioritized for carrier/station follow-up and revised ETA communication."
    )
