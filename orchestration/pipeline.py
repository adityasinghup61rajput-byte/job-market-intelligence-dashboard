from src.ingestion import ingest_file
from src.transform import transform_with_pandas
from src.quality import run_quality_checks
from src.database import build_warehouse

def run():
    ingest_file()
    transform_with_pandas()
    report = run_quality_checks()
    build_warehouse()
    print("Pipeline completed successfully.")
    print(report)

if __name__ == "__main__":
    run()
