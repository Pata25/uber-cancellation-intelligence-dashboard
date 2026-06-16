-- Question:
-- How much revenue is lost due to ride cancellations?

SELECT
    city_name,
    COUNT(*) FILTER (WHERE ride_status = 'cancelled') AS cancelled_rides,
    SUM(
        CASE
            WHEN ride_status = 'cancelled'
            THEN estimated_fare
            ELSE 0
        END
    ) AS estimated_revenue_lost
FROM uber.rides
GROUP BY city_name
ORDER BY estimated_revenue_lost DESC;
