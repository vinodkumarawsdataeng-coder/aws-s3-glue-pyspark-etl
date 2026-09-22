# 🧱 AWS Customer Data ETL Pipeline

This project demonstrates a simple end-to-end data engineering pipeline
using AWS services to ingest customer data from Amazon S3, process it
using AWS Glue and PySpark, and store the transformed data back in S3
as partitioned Parquet files.

The project focuses on common data engineering practices such as data
cleaning, duplicate handling, data validation, transformation,
partitioning, and columnar data storage.

## 📊 Dataset

The project uses a sample customer dataset in CSV format.

The dataset contains the following fields:

- Customer ID
- Customer Name
- City
- Age
- Salary

The sample dataset contains customer records with different cities,
ages, and salary values.

The original CSV file is available in the `data` folder.

## 🛠️ Tools and Technologies

- **Amazon S3** - Stores raw and processed data.
- **AWS Glue** - Runs the ETL job.
- **PySpark** - Performs data cleaning and transformations.
- **Python** - Used for the Glue ETL script.
- **Amazon CloudWatch** - Used for monitoring Glue job logs.
- **IAM** - Controls access to AWS resources.
- **Parquet** - Used as the output data format.

## 🧩 Architecture Overview

The pipeline follows a simple raw-to-curated data flow:


                    Customer CSV
                         |
                         v
              Amazon S3 - Raw Layer
                         |
                         v
                 AWS Glue + PySpark
                         |
              +----------+----------+
              |          |          |
              v          v          v
           Cleaning   Validation  Transformations
              |          |          |
              +----------+----------+
                         |
                         v
             Amazon S3 - Curated Layer
                         |
                         v
                  Parquet Files
                         |
                  Partitioned by City

                  
🔄 Workflow
1. Data Ingestion

The customer CSV file is uploaded to the raw S3 location.

Example:

s3://s3-to-s3-etl-job/raw/customers/

The raw layer keeps the original source data before transformation.

2. Read Data Using AWS Glue

The AWS Glue PySpark job reads the CSV file from the S3 raw location.

The ETL job uses an explicit schema for the customer data instead of
depending on automatic schema inference.

The schema contains:

customer_id
name
city
age
salary
3. Data Cleaning

The Glue job performs basic data cleaning.

The following operations are performed:

Remove records with missing required fields.
Remove duplicate customer records.
Remove extra spaces from names.
Standardize city names.
4. Data Validation

Basic data quality checks are performed during processing.

The job checks for:

Missing customer IDs
Invalid age values
Negative salary values
Duplicate customer records

The validation results are written to the Glue job logs.

5. Data Transformation

Additional columns are created during the transformation process.

Salary Category

Salary values are classified into:

HIGH
MEDIUM
LOW
Age Category

Customers are classified into:

YOUNG
MIDDLE
SENIOR

The ETL job also adds a processing_date column.

6. Store Curated Data

After transformation, the processed data is written back to Amazon S3.

The output is stored in Parquet format.

Example:

s3://s3-to-s3-etl-job/curated/customers/

The data is partitioned by city:

curated/customers/
    city=Bangalore/
    city=Chennai/
    city=Delhi/
    city=Hyderabad/
    city=Mumbai/

Partitioning makes it easier to filter and process data based on city.


🧪 Data Validation Queries

SQL queries are included in:

sql/validation_queries.sql

The queries can be used to validate:

Total customer records
Duplicate customer IDs
NULL values
Invalid ages
Invalid salaries
Customer count by city
Average salary by city
Salary category distribution
Age category distribution
📜 Glue ETL Script

The main ETL script is available here:

glue/etl_job.py

The script handles:

Reading data from S3.
Applying the schema.
Cleaning the data.
Removing duplicates.
Performing data quality checks.
Creating derived columns.
Writing Parquet output.
Partitioning the output by city.
Logging ETL results.
📈 Output

The final dataset contains:

customer_id
name
city
age
age_category
salary
salary_category
processing_date

The output is stored as partitioned Parquet files in the S3 curated
layer.

🔐 Security

No AWS credentials, passwords, access keys, or secret values are stored
in this repository.

AWS IAM is used to provide the required permissions to the Glue job.

S3 bucket names and environment-specific paths are passed through Glue
job parameters rather than hardcoded in the ETL script.
