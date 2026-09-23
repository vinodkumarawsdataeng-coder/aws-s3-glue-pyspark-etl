-- 1.Check how many customer records we have
SELECT COUNT(*) AS total_customers
FROM customers;


-- 2.Check if any customer_id appears more than once
SELECT customer_id, COUNT(*) AS cnt
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


--3.Check for missing customer IDs
SELECT COUNT(*) AS null_customer_ids
FROM customers
WHERE customer_id IS NULL;


-- 4.Check for missing customer names
SELECT COUNT(*) AS null_names
FROM customers
WHERE name IS NULL;


-- 5.Find customers with an invalid age
SELECT customer_id, name, age
FROM customers
WHERE age < 18
   OR age > 100;


--6. Find records with a negative salary
SELECT customer_id, name, salary
FROM customers
WHERE salary < 0;


--7. See how many customers are in each city
SELECT city, COUNT(*) AS customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC;


-- 8.Compare average salary across cities
SELECT
    city,
    ROUND(AVG(salary), 2) AS avg_salary
FROM customers
GROUP BY city
ORDER BY avg_salary DESC;


-- 9.Check the number of customers in each salary category
SELECT
    salary_category,
    COUNT(*) AS customer_count
FROM customers
GROUP BY salary_category
ORDER BY customer_count DESC;


-- 10.Check the number of customers in each age group
SELECT
    age_category,
    COUNT(*) AS customer_count
FROM customers
GROUP BY age_category
ORDER BY customer_count DESC;
