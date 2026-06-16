-- Question:
-- What are the most common reasons riders cancel Uber rides?

SELECT
    cancellation_reason,
    COUNT(*) AS total
FROM uber.rides
WHERE cancellation_reason IS NOT NULL
GROUP BY cancellation_reason
ORDER BY total DESC;
