-- Question:
-- Which city has the highest cancellation rate?

SELECT
    city_name,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN ride_status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_rides,
    ROUND(
        100.0 * SUM(CASE WHEN ride_status = 'cancelled' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS cancellation_rate
FROM uber.rides
GROUP BY city_name
ORDER BY cancellation_rate DESC;
