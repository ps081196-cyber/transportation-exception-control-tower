-- 1. Stations with the highest exception rate
SELECT station,
       COUNT(*) AS shipments,
       SUM(CASE WHEN status = 'Exception' THEN 1 ELSE 0 END) AS open_exceptions,
       100.0 * SUM(CASE WHEN status = 'Exception' THEN 1 ELSE 0 END) / COUNT(*) AS exception_rate_pct
FROM transportation_events
GROUP BY station
ORDER BY exception_rate_pct DESC;

-- 2. SLA-breached cases requiring immediate follow-up
SELECT shipment_id, station, carrier, exception_reason,
       exception_age_hours, customer_contacts
FROM transportation_events
WHERE status = 'Exception'
  AND exception_age_hours > 4
ORDER BY exception_age_hours DESC;

-- 3. Root-cause Pareto analysis
SELECT exception_reason, COUNT(*) AS cases
FROM transportation_events
WHERE status = 'Exception'
GROUP BY exception_reason
ORDER BY cases DESC;

-- 4. Carrier performance
SELECT carrier,
       COUNT(*) AS shipments,
       AVG(CASE WHEN actual_or_expected_delivery <= promised_delivery THEN 1.0 ELSE 0.0 END) AS on_time_rate
FROM transportation_events
GROUP BY carrier
ORDER BY on_time_rate DESC;
