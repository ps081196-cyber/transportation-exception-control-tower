# Transportation Exception Control Tower

Portfolio project tailored to Amazon's **Transportation Representative, IN Channel Support** role (Job ID 10418348).

## Business scenario

A Network Operations Center supports last-mile stations, carriers and cross-functional teams. The control tower detects transportation exceptions, prioritizes cases by customer impact, tracks response SLAs, recommends next actions and produces stakeholder-ready updates.

## Capabilities demonstrated

- Last-mile network monitoring and exception management
- SLA-based prioritization and escalation
- Trend analysis by station, carrier, route and root cause
- Clear written stakeholder communication
- Process-improvement opportunity identification
- Excel-ready exports, SQL analysis and Python automation

## Dashboard

- Network health KPIs: on-time %, open cases, critical cases and SLA compliance
- Live exception queue with severity and recommended action
- Station/carrier performance comparison
- Root-cause Pareto chart
- Automatically generated stakeholder update
- Downloadable case-management report

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The project creates reproducible synthetic transportation data, so no confidential company data is required.

## Test

```bash
pytest -q
```

## Project structure

- `app.py` — Streamlit NOC dashboard
- `control_tower.py` — KPI, SLA, prioritization and communication logic
- `generate_data.py` — realistic sample-data generator
- `sql/analysis_queries.sql` — SQL queries for operational reviews
- `tests/` — automated business-logic tests
- `INTERVIEW_GUIDE.md` — project explanation and resume bullets

## Job alignment

| Job requirement | Project evidence |
|---|---|
| Transportation execution | Shipment-level last-mile monitoring |
| Resolve exceptions | Priority queue and recommended actions |
| Keep stakeholders informed | Auto-generated written network update |
| Analyze trends | Station, carrier and root-cause analytics |
| Process improvement | Repeat-issue and Pareto analysis |
| Excel and SQL | CSV export and operational SQL query pack |

## Technology

Python · pandas · Streamlit · Plotly · SQL · pytest

This is an original portfolio simulation and is not an Amazon internal tool.
