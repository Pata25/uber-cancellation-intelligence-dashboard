-- Question:
-- Does ETA impact ride cancellations?

SELECT
    CASE
        WHEN eta_minutes <= 5 THEN '0-5 min'
        WHEN eta_minutes <= 10 THEN '6-10 min'
        WHEN eta_minutes <= 15 THEN '11-15 min'
        ELSE '16+ min'
    END AS eta_bucket,

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
GROUP BY eta_bucket
ORDER BY eta_bucket;
