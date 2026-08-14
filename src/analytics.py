import sqlite3
import pandas as pd
from src.config import DB_PATH

def query(sql, params=()):
    with sqlite3.connect(DB_PATH) as con:
        return pd.read_sql_query(sql, con, params=params)

def summary():
    return query("SELECT COUNT(*) total_jobs, ROUND(AVG(salary_avg),0) avg_salary, ROUND(MAX(salary_avg),0) max_avg_salary FROM fact_job_posting")

def jobs_by_location():
    return query("""SELECT l.location, COUNT(*) jobs
                    FROM fact_job_posting f JOIN dim_location l
                    ON f.location_key=l.location_key
                    GROUP BY l.location ORDER BY jobs DESC""")

def jobs_by_title():
    return query("""SELECT t.job_title, COUNT(*) jobs
                    FROM fact_job_posting f JOIN dim_title t
                    ON f.title_key=t.title_key
                    GROUP BY t.job_title ORDER BY jobs DESC LIMIT 10""")

def salary_by_location():
    return query("""SELECT l.location, ROUND(AVG(f.salary_avg),0) avg_salary
                    FROM fact_job_posting f JOIN dim_location l
                    ON f.location_key=l.location_key
                    GROUP BY l.location ORDER BY avg_salary DESC""")
