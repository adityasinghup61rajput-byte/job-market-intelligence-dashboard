import json
import pandas as pd
from src.config import STAGING_DIR, LOG_DIR

def run_quality_checks():
    df = pd.read_csv(STAGING_DIR / "jobs_clean.csv")
    checks = {
        "row_count": int(len(df)),
        "unique_job_ids": int(df["job_id"].nunique()),
        "duplicate_job_ids": int(df["job_id"].duplicated().sum()),
        "null_job_ids": int(df["job_id"].isna().sum()),
        "invalid_salary_ranges": int((df["salary_min"] > df["salary_max"]).sum()),
        "null_posted_dates": int(df["posted_date"].isna().sum()),
        "quality_passed": bool(df["job_id"].notna().all()
                               and df["job_id"].is_unique
                               and (df["salary_min"] <= df["salary_max"]).all())
    }
    with open(LOG_DIR / "quality_report.json", "w") as f:
        json.dump(checks, f, indent=2)
    if not checks["quality_passed"]:
        raise ValueError(f"Data quality failed: {checks}")
    return checks

if __name__ == "__main__":
    print(run_quality_checks())
