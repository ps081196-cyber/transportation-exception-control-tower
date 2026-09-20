from control_tower import enrich_cases, exception_queue, network_kpis, stakeholder_update
from generate_data import generate_shipments

def test_control_tower_pipeline():
    data = enrich_cases(generate_shipments(300, 7), sla_hours=4)
    kpis = network_kpis(data)
    queue = exception_queue(data)
    assert 0 <= kpis["on_time_rate"] <= 1
    assert 0 <= kpis["sla_compliance"] <= 1
    assert len(queue) == kpis["open_exceptions"]
    assert queue.iloc[0].priority in {"High", "Critical", "Medium"}

def test_stakeholder_update_contains_operational_metrics():
    data = enrich_cases(generate_shipments(100, 3))
    update = stakeholder_update(data)
    assert "open transportation exceptions" in update
    assert "SLA compliance" in update
