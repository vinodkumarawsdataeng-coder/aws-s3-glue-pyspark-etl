import sys
import logging

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import (StructType,StructField,IntegerType,StringType,DoubleType)

# Job parameters
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "INPUT_PATH", "OUTPUT_PATH"]
)

job_name = args["JOB_NAME"]
input_path = args["INPUT_PATH"]
output_path = args["OUTPUT_PATH"]

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create Glue and Spark context
sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(job_name, args)


try:
    logger.info("Starting customer ETL job")
    logger.info(f"Reading data from: {input_path}")

    # Define schema
    customer_schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("salary", DoubleType(), True)
    ])
    # Read CSV from S3
    df = (
        spark.read
        .option("header", "true")
        .schema(customer_schema)
        .csv(input_path)
    )
    source_count = df.count()
    logger.info(f"Source record count: {source_count}")

    # Remove records with missing mandatory fields
    df = df.dropna(
        subset=["customer_id", "name", "city"]
    )

    # Remove duplicate customers
    df = df.dropDuplicates(["customer_id"])

    # Clean string columns
    df = (
        df.withColumn("name", F.trim(F.col("name")))
          .withColumn("city", F.initcap(F.trim(F.col("city"))))
    )

    # Add salary category
    df = df.withColumn(
        "salary_category",
        F.when(F.col("salary") >= 80000, "HIGH")
         .when(F.col("salary") >= 60000, "MEDIUM")
         .otherwise("LOW")
    )

    # Add age category
    df = df.withColumn(
        "age_category",
        F.when(F.col("age") < 30, "YOUNG")
         .when(F.col("age") <= 45, "MIDDLE")
         .otherwise("SENIOR")
    )

    # Add processing date
    df = df.withColumn(
        "processing_date",
        F.current_date()
    )

    # Data quality checks
    invalid_age_count = df.filter(
        (F.col("age") < 18) | (F.col("age") > 100)
    ).count()

    invalid_salary_count = df.filter(
        F.col("salary") < 0
    ).count()

    logger.info(f"Invalid age records: {invalid_age_count}")
    logger.info(f"Invalid salary records: {invalid_salary_count}")

    # Select final columns
    final_df = df.select(
        "customer_id",
        "name",
        "city",
        "age",
        "age_category",
        "salary",
        "salary_category",
        "processing_date"
    )

    final_count = final_df.count()
    logger.info(f"Final record count: {final_count}")

    # Write curated data to S3
    (
        final_df.write
        .mode("overwrite")
        .format("parquet")
        .partitionBy("city")
        .save(output_path)
    )

    logger.info(
        f"Successfully written data to: {output_path}"
    )

    job.commit()

    logger.info("Customer ETL job completed successfully")

except Exception as e:
    logger.error(
        f"Customer ETL job failed: {str(e)}",exc_info=True)
    raise