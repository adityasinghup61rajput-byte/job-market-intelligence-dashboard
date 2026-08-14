-- Cloud Job Market Intelligence: Data Quality SQL

-- 1. Fact row count
SELECT COUNT(*) AS fact_row_count
FROM fact_job_posting;

-- 2. Duplicate job IDs
SELECT job_id, COUNT(*) AS duplicate_count
FROM fact_job_posting
GROUP BY job_id
HAVING COUNT(*) > 1;

-- 3. Null job IDs
SELECT COUNT(*) AS null_job_ids
FROM fact_job_posting
WHERE job_id IS NULL;

-- 4. Invalid salary ranges
SELECT COUNT(*) AS invalid_salary_ranges
FROM fact_job_posting
WHERE salary_min > salary_max;

-- 5. Salary average consistency
SELECT COUNT(*) AS inconsistent_salary_avg
FROM fact_job_posting
WHERE salary_avg IS NOT NULL
  AND (salary_avg < salary_min OR salary_avg > salary_max);

-- 6. Orphan company keys
SELECT COUNT(*) AS orphan_company_keys
FROM fact_job_posting f
LEFT JOIN dim_company d ON f.company_key = d.company_key
WHERE d.company_key IS NULL;

-- 7. Orphan location keys
SELECT COUNT(*) AS orphan_location_keys
FROM fact_job_posting f
LEFT JOIN dim_location d ON f.location_key = d.location_key
WHERE d.location_key IS NULL;

-- 8. Orphan title keys
SELECT COUNT(*) AS orphan_title_keys
FROM fact_job_posting f
LEFT JOIN dim_title d ON f.title_key = d.title_key
WHERE d.title_key IS NULL;

-- 9. Orphan date keys
SELECT COUNT(*) AS orphan_date_keys
FROM fact_job_posting f
LEFT JOIN dim_date d ON f.date_key = d.date_key
WHERE d.date_key IS NULL;

-- 10. Reconciliation
SELECT COUNT(*) AS fact_rows,
       COUNT(DISTINCT job_id) AS unique_jobs,
       COUNT(*) - COUNT(DISTINCT job_id) AS duplicate_difference
FROM fact_job_posting;
