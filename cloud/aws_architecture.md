# AWS Deployment Blueprint

| Local | AWS |
|---|---|
| data/raw | Amazon S3 |
| PySpark | AWS Glue or EMR |
| Curated Parquet | S3 |
| Warehouse | Redshift |
| SQL | Athena |
| Orchestration | Step Functions / MWAA |
| Monitoring | CloudWatch |
| Secrets | Secrets Manager |
| GenAI | Amazon Bedrock |

Production flow:
S3 Raw → Glue Spark → S3 Curated → Redshift/Athena → Dashboard.

Use IAM roles and least privilege. Never hard-code cloud credentials.
