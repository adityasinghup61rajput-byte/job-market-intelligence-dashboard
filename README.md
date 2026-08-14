# Cloud Job Market Intelligence Lakehouse

End-to-end Cloud Data Engineering capstone aligned to the uploaded Cloud Data Engineer Trainee JD.

## Covers
- File/API-style ingestion
- Bronze/Silver/Gold layers
- PySpark + Pandas processing
- Star-schema dimensional modeling
- SQL analytics, joins, CTEs and window functions
- Data quality, validation and reconciliation
- Parquet data-lake storage
- Logging and testing
- Streamlit dashboard
- GenAI-ready insight generation
- AWS production architecture

## Architecture
CSV/API -> Bronze -> Silver -> Gold Parquet -> Star Schema Warehouse -> SQL Analytics -> Dashboard -> GenAI

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python orchestration/pipeline.py
streamlit run app.py
```

If Spark/Java is not configured, the pipeline uses the Pandas fallback. For Spark practice:
```bash
python src/transform_spark.py
```

## AWS mapping
S3 -> Glue/EMR -> S3 Parquet -> Redshift/Athena -> Step Functions/MWAA -> CloudWatch -> Bedrock.
