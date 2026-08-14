import sqlite3
import pandas as pd
from src.config import DB_PATH, STAGING_DIR

SCHEMA = """
DROP TABLE IF EXISTS fact_job_posting;
DROP TABLE IF EXISTS dim_company;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS dim_title;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_company (
    company_key INTEGER PRIMARY KEY,
    company TEXT UNIQUE NOT NULL
);
CREATE TABLE dim_location (
    location_key INTEGER PRIMARY KEY,
    location TEXT UNIQUE NOT NULL
);
CREATE TABLE dim_title (
    title_key INTEGER PRIMARY KEY,
    job_title TEXT UNIQUE NOT NULL
);
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT UNIQUE NOT NULL,
    year INTEGER, month INTEGER, day INTEGER
);
CREATE TABLE fact_job_posting (
    job_key INTEGER PRIMARY KEY,
    job_id TEXT UNIQUE NOT NULL,
    company_key INTEGER, location_key INTEGER, title_key INTEGER, date_key INTEGER,
    experience TEXT, salary_min REAL, salary_max REAL, salary_avg REAL,
    employment_type TEXT, source TEXT
);
"""

def build_warehouse():
    df = pd.read_csv(STAGING_DIR / "jobs_clean.csv")
    df["posted_date"] = pd.to_datetime(df["posted_date"])
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)

    companies = pd.DataFrame({"company": sorted(df["company"].unique())})
    companies.insert(0, "company_key", range(1, len(companies)+1))
    companies.to_sql("dim_company", con, if_exists="append", index=False)

    locations = pd.DataFrame({"location": sorted(df["location"].unique())})
    locations.insert(0, "location_key", range(1, len(locations)+1))
    locations.to_sql("dim_location", con, if_exists="append", index=False)

    titles = pd.DataFrame({"job_title": sorted(df["job_title"].unique())})
    titles.insert(0, "title_key", range(1, len(titles)+1))
    titles.to_sql("dim_title", con, if_exists="append", index=False)

    dates = pd.DataFrame({"full_date": sorted(df["posted_date"].dt.strftime("%Y-%m-%d").unique())})
    dates.insert(0, "date_key", range(1, len(dates)+1))
    dt = pd.to_datetime(dates["full_date"])
    dates["year"], dates["month"], dates["day"] = dt.dt.year, dt.dt.month, dt.dt.day
    dates.to_sql("dim_date", con, if_exists="append", index=False)

    c = dict(zip(companies.company, companies.company_key))
    l = dict(zip(locations.location, locations.location_key))
    t = dict(zip(titles.job_title, titles.title_key))
    d = dict(zip(dates.full_date, dates.date_key))

    fact = df.copy()
    fact["company_key"] = fact["company"].map(c)
    fact["location_key"] = fact["location"].map(l)
    fact["title_key"] = fact["job_title"].map(t)
    fact["date_key"] = fact["posted_date"].dt.strftime("%Y-%m-%d").map(d)
    fact.insert(0, "job_key", range(1, len(fact)+1))
    cols = ["job_key","job_id","company_key","location_key","title_key","date_key",
            "experience","salary_min","salary_max","salary_avg","employment_type","source"]
    fact[cols].to_sql("fact_job_posting", con, if_exists="append", index=False)
    con.close()

if __name__ == "__main__":
    build_warehouse()
