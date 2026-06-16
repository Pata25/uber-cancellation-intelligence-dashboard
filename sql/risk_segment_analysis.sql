-- Question:
-- Which ride segments have the highest cancellation risk?

SELECT
    CASE
        WHEN eta_minutes <= 10 THEN 'Low ETA'
        ELSE 'High ETA'
    END AS eta_group,

    CASE
        WHEN surge_multiplier <= 1.5 THEN 'Low Surge'
        ELSE 'High Surge'
    END AS surge_group,

    COUNT(*) AS total_rides,

    SUM(
        CASE
            WHEN ride_status = 'cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_rides,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN ride_status = 'cancelled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate_pct

FROM uber.rides
GROUP BY eta_group, surge_group
ORDER BY eta_group, surge_group;
