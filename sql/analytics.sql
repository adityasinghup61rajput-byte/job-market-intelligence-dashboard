-- Total jobs
SELECT COUNT(*) AS total_jobs FROM fact_job_posting;

-- Average salary by location
SELECT l.location, ROUND(AVG(f.salary_avg),0) avg_salary
FROM fact_job_posting f JOIN dim_location l ON f.location_key=l.location_key
GROUP BY l.location ORDER BY avg_salary DESC;

-- Top companies
SELECT c.company, COUNT(*) job_count
FROM fact_job_posting f JOIN dim_company c ON f.company_key=c.company_key
GROUP BY c.company ORDER BY job_count DESC;

-- Window function
SELECT l.location, t.job_title, f.salary_avg,
       RANK() OVER(PARTITION BY l.location ORDER BY f.salary_avg DESC) salary_rank
FROM fact_job_posting f
JOIN dim_location l ON f.location_key=l.location_key
JOIN dim_title t ON f.title_key=t.title_key;

-- Reconciliation
SELECT COUNT(*) AS warehouse_rows FROM fact_job_posting;
