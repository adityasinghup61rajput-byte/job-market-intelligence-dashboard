-- Cloud Job Market Intelligence: SQL Analytics
-- SQLite-compatible queries

-- 1. Jobs by location
SELECT l.location, COUNT(*) AS total_jobs
FROM fact_job_posting f
JOIN dim_location l ON f.location_key = l.location_key
GROUP BY l.location
ORDER BY total_jobs DESC;

-- 2. Average salary by location
SELECT l.location,
       ROUND(AVG(f.salary_avg), 0) AS avg_salary,
       COUNT(*) AS jobs
FROM fact_job_posting f
JOIN dim_location l ON f.location_key = l.location_key
GROUP BY l.location
ORDER BY avg_salary DESC;

-- 3. Highest-paying job titles
SELECT t.job_title,
       ROUND(AVG(f.salary_avg), 0) AS avg_salary,
       COUNT(*) AS jobs
FROM fact_job_posting f
JOIN dim_title t ON f.title_key = t.title_key
GROUP BY t.job_title
ORDER BY avg_salary DESC;

-- 4. Company hiring analysis
SELECT c.company,
       COUNT(*) AS job_postings,
       ROUND(AVG(f.salary_avg), 0) AS avg_salary
FROM fact_job_posting f
JOIN dim_company c ON f.company_key = c.company_key
GROUP BY c.company
ORDER BY job_postings DESC, avg_salary DESC;

-- 5. Window function: salary rank within location
WITH salary_data AS (
    SELECT l.location, t.job_title, f.salary_avg
    FROM fact_job_posting f
    JOIN dim_location l ON f.location_key = l.location_key
    JOIN dim_title t ON f.title_key = t.title_key
)
SELECT location, job_title, salary_avg,
       RANK() OVER (
           PARTITION BY location
           ORDER BY salary_avg DESC
       ) AS salary_rank
FROM salary_data
ORDER BY location, salary_rank;

-- 6. CTE: locations above overall average salary
WITH location_salary AS (
    SELECT l.location, AVG(f.salary_avg) AS avg_salary
    FROM fact_job_posting f
    JOIN dim_location l ON f.location_key = l.location_key
    GROUP BY l.location
)
SELECT location, ROUND(avg_salary, 0) AS avg_salary
FROM location_salary
WHERE avg_salary > (SELECT AVG(salary_avg) FROM fact_job_posting)
ORDER BY avg_salary DESC;

-- 7. CASE: salary bands
SELECT t.job_title, f.salary_avg,
       CASE
           WHEN f.salary_avg >= 1500000 THEN 'High'
           WHEN f.salary_avg >= 1000000 THEN 'Medium'
           ELSE 'Entry'
       END AS salary_band
FROM fact_job_posting f
JOIN dim_title t ON f.title_key = t.title_key
ORDER BY f.salary_avg DESC;

-- 8. Hiring trend by date
SELECT d.full_date AS posted_date, COUNT(*) AS jobs
FROM fact_job_posting f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.full_date
ORDER BY d.full_date;

-- 9. Location + title analysis
SELECT l.location, t.job_title, COUNT(*) AS jobs
FROM fact_job_posting f
JOIN dim_location l ON f.location_key = l.location_key
JOIN dim_title t ON f.title_key = t.title_key
GROUP BY l.location, t.job_title
ORDER BY l.location, jobs DESC;

-- 10. Top 5 titles by salary
SELECT t.job_title, ROUND(AVG(f.salary_avg), 0) AS avg_salary
FROM fact_job_posting f
JOIN dim_title t ON f.title_key = t.title_key
GROUP BY t.job_title
ORDER BY avg_salary DESC
LIMIT 5;
