import pandas as pd
from pyspark.sql import SparkSession, functions as F
from src.config import RAW_DIR, CURATED_DIR


def run_spark():
    spark = (
        SparkSession.builder
        .appName("CloudJobMarketPipeline")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    # Read raw data with Spark
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW_DIR / "jobs.csv"))
    )

    # Spark transformations
    df = (
        df.dropDuplicates(["job_id"])
        .withColumn("posted_date", F.to_date("posted_date"))
        .withColumn(
            "salary_avg",
            (F.col("salary_min") + F.col("salary_max")) / 2
        )
        .withColumn("year", F.year("posted_date"))
        .withColumn("month", F.month("posted_date"))
    )

    print("\nJobs by Location:")
    (
        df.groupBy("location")
        .count()
        .orderBy(F.desc("count"))
        .show(10, truncate=False)
    )

    # Convert Spark DataFrame to Pandas
    result = df.toPandas()

    # Save using Pandas instead of Spark writer.
    # This avoids the Windows winutils.exe problem.
    output_dir = CURATED_DIR / "spark_jobs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "jobs.csv"
    result.to_csv(output_file, index=False)

    print("\n========================================")
    print("✅ PySpark transformation completed!")
    print(f"✅ Rows processed: {len(result)}")
    print(f"✅ Output: {output_file}")
    print("========================================")

    spark.stop()


if __name__ == "__main__":
    run_spark()