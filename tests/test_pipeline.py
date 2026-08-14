from pathlib import Path
import pandas as pd

def test_raw_schema():
    df = pd.read_csv("data/raw/jobs.csv")
    required = {"job_id","job_title","company","location","experience","salary_min",
                "salary_max","employment_type","posted_date","skills","source"}
    assert required.issubset(df.columns)

def test_salary_range():
    df = pd.read_csv("data/raw/jobs.csv")
    assert (df["salary_min"] <= df["salary_max"]).all()

def test_job_id_unique():
    df = pd.read_csv("data/raw/jobs.csv")
    assert df["job_id"].is_unique
