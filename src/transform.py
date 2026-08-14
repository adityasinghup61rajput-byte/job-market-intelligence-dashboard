import logging
import pandas as pd
from src.config import RAW_DIR, STAGING_DIR, CURATED_DIR, LOG_DIR

logging.basicConfig(filename=LOG_DIR / "pipeline.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

def transform_with_pandas():
    df = pd.read_csv(RAW_DIR / "jobs.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.drop_duplicates(subset=["job_id"]).copy()
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    for col in ["job_title","company","location","employment_type","source"]:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    df["skills"] = df["skills"].fillna("").astype(str)
    df.to_csv(STAGING_DIR / "jobs_clean.csv", index=False)
    df.to_parquet(CURATED_DIR / "jobs_curated.parquet", index=False)
    logging.info("Transformed %s rows", len(df))
    return df

if __name__ == "__main__":
    transform_with_pandas()
