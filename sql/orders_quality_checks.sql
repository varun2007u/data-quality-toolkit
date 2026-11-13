-- Illustrative warehouse-side controls for an orders table.
-- Replace analytics.orders with the table name in your environment.

-- 1. Duplicate business keys
SELECT order_id, COUNT(*) AS row_count
FROM analytics.orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. Missing identifiers and required attributes
SELECT *
FROM analytics.orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR order_date IS NULL
   OR status IS NULL;

-- 3. Status values outside the agreed domain
SELECT *
FROM analytics.orders
WHERE status NOT IN ('pending', 'completed', 'cancelled', 'refunded');

-- 4. Invalid amounts
SELECT *
FROM analytics.orders
WHERE amount IS NULL OR amount < 0;

-- 5. Reconciliation: row count and amount by status
SELECT status, COUNT(*) AS order_count, SUM(amount) AS total_amount
FROM analytics.orders
GROUP BY status
ORDER BY status;
