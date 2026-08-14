import logging
from pathlib import Path
import pandas as pd
from src.config import RAW_DIR, LOG_DIR

logging.basicConfig(filename=LOG_DIR / "pipeline.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

REQUIRED = ["job_id","job_title","company","location","experience","salary_min",
            "salary_max","employment_type","posted_date","skills","source"]

def ingest_file(path=None):
    path = Path(path) if path else RAW_DIR / "jobs.csv"
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    logging.info("Ingested %s rows from %s", len(df), path)
    return df

if __name__ == "__main__":
    ingest_file()
