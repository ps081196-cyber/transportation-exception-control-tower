import pandas as pd
import plotly.express as px
import streamlit as st
from control_tower import enrich_cases, exception_queue, network_kpis, stakeholder_update
from generate_data import generate_shipments

st.set_page_config(page_title="Transportation Exception Control Tower", page_icon="🚚", layout="wide")
st.title("🚚 Transportation Exception Control Tower")
st.caption("Last-mile network monitoring, SLA management and stakeholder communication")

upload = st.sidebar.file_uploader("Upload transportation CSV", type="csv")
sla = st.sidebar.slider("Response SLA (hours)", 1, 12, 4)
raw = pd.read_csv(upload) if upload else generate_shipments()
data = enrich_cases(raw, sla)

stations = st.sidebar.multiselect("Station", sorted(data.station.unique()), default=sorted(data.station.unique()))
filtered = data[data.station.isin(stations)]
kpi = network_kpis(filtered)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Shipments", f"{kpi['shipments']:,}")
c2.metric("On-time rate", f"{kpi['on_time_rate']:.1%}")
c3.metric("Open exceptions", kpi["open_exceptions"])
c4.metric("Critical cases", kpi["critical_cases"])
c5.metric("SLA compliance", f"{kpi['sla_compliance']:.1%}")

st.subheader("Stakeholder update")
st.info(stakeholder_update(filtered))

left, right = st.columns(2)
with left:
    causes = filtered[filtered.open_exception].groupby("exception_reason", as_index=False).size().sort_values("size")
    st.plotly_chart(px.bar(causes, x="size", y="exception_reason", orientation="h", title="Exception Pareto"), use_container_width=True)
with right:
    station_perf = filtered.groupby("station", as_index=False).agg(open_exceptions=("open_exception", "sum"), late_rate=("late", "mean"))
    st.plotly_chart(px.scatter(station_perf, x="open_exceptions", y="late_rate", text="station", size="open_exceptions", title="Station risk map"), use_container_width=True)

st.subheader("Live exception queue")
queue = exception_queue(filtered)
st.dataframe(queue, use_container_width=True, hide_index=True)
st.download_button("Download case-management report", queue.to_csv(index=False), "transportation_exception_queue.csv", "text/csv")

with st.expander("Carrier performance"):
    carrier = filtered.groupby("carrier", as_index=False).agg(shipments=("shipment_id", "count"), on_time_rate=("late", lambda x: 1-x.mean()), exceptions=("open_exception", "sum"))
    st.dataframe(carrier.style.format({"on_time_rate": "{:.1%}"}), use_container_width=True, hide_index=True)
