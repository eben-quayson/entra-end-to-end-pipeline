{{ config(materialized='view') }}
SELECT
    trip_date,
    COUNT(*) AS trip_count,
    SUM(fare) AS total_revenue
FROM trips
GROUP BY trip_date
ORDER BY trip_date