-- Question:
-- What is the overall cancellation rate of Uber rides?

SELECT
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

FROM uber.rides;
