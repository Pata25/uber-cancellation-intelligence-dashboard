-- Question:
-- Does surge pricing impact ride cancellations?

SELECT
    CASE
        WHEN surge_multiplier = 1 THEN 'No Surge'
        WHEN surge_multiplier <= 1.5 THEN 'Low Surge'
        WHEN surge_multiplier <= 2 THEN 'Medium Surge'
        ELSE 'High Surge'
    END AS surge_bucket,

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
GROUP BY surge_bucket
ORDER BY surge_bucket;
