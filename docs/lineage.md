# Data Lineage

jobs.csv / API
→ ingestion.py
→ Bronze raw
→ transform.py or transform_spark.py
→ Silver staging
→ Gold Parquet
→ database.py
→ Star Schema Warehouse
→ analytics.py
→ Streamlit
→ GenAI insight layer

## Quality
Required columns, duplicate detection, salary validation, date parsing,
standardization, reconciliation and pipeline logging.
