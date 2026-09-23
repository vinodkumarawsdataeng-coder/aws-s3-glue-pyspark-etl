# 🧱 AWS Customer Data ETL Pipeline

This project demonstrates an end-to-end data engineering pipeline using AWS services to ingest customer data from Amazon S3, process it using AWS Glue and PySpark, store the transformed data as partitioned Parquet files in Amazon S3, and query the curated data using Amazon Athena.

The project focuses on common data engineering practices such as data cleaning, duplicate handling, data validation, data transformation, partitioning, columnar storage, metadata management, and SQL-based data analysis.

## 📊 Dataset

The project uses a sample customer dataset in CSV format.

The dataset contains the following fields:

- Customer ID
- Customer Name
- City
- Age
- Salary

The original CSV file is available in the `data` folder.

Example:
customer_id
name
city
age
salary

## 🧩 Architecture Overview

The pipeline follows a raw-to-curated data flow with Athena used for querying the curated data.

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
              Partitioned Parquet Files
                  Partitioned by City
                         |
                         v
             AWS Glue Data Catalog
                  (Table Metadata)
                         |
                         v
                  Amazon Athena
                         |
                         v
                  SQL Analysis

### 🔄 Workflow

## 1. Data Ingestion

The customer CSV file is uploaded to the raw S3 location.

s3://s3-to-s3-etl-jobs/raw/customers/

The raw layer keeps the original source data before transformation.

Example:

raw/
└── customers/
    └── customers.csv
    
## 2. Read Data Using AWS Glue

The AWS Glue PySpark job reads the CSV file directly from the S3 raw location.

The ETL job uses an explicit schema instead of relying on automatic schema inference.

The schema contains:

customer_id
name
city
age
salary

The Glue job receives the input and output S3 paths through job parameters.

Example:

--INPUT_PATH
s3://s3-to-s3-etl-jobs/raw/customers/

--OUTPUT_PATH
s3://s3-to-s3-etl-jobs/curated/customers/

## 3. Data Cleaning

The Glue PySpark job performs basic data cleaning.

The following operations are performed:

Remove records with missing required fields.
Remove duplicate customer records.
Trim extra spaces from customer names.
Standardize city names.

For duplicate handling, customer_id is used to identify duplicate customer records.

## 4. Data Validation

Basic data quality checks are performed during processing.

The job checks for:

Missing customer IDs.
Invalid age values.
Negative salary values.
Duplicate customer records.

The validation results are written to the AWS Glue job logs.

Example log information includes:

Source record count
Invalid age records
Invalid salary records
Final record count
ETL job status

## 5. Data Transformation

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

The ETL job also adds:

processing_date

## 6. Store Curated Data

After transformation, the processed data is written back to Amazon S3.

The output is stored in Parquet format.

s3://s3-to-s3-etl-jobs/curated/customers/

The data is partitioned by city.

Example:

curated/
└── customers/
    ├── city=Ahmedabad/
    ├── city=Bangalore/
    ├── city=Chennai/
    ├── city=Delhi/
    ├── city=Hyderabad/
    ├── city=Jaipur/
    ├── city=Kochi/
    ├── city=Kolkata/
    ├── city=Mumbai/
    └── city=Pune/

Each partition contains Parquet files similar to:

part-00000-xxxx.snappy.parquet

Partitioning by city makes it more efficient to query data for a specific city.

For example:

SELECT *
FROM customers
WHERE city = 'Bangalore';

## 🗂️ 7. AWS Glue Data Catalog

The project uses the AWS Glue Data Catalog to store metadata for the curated customer dataset.

A database was created:

customer_etl_db

A table was created:

customers

The table points to:

s3://s3-to-s3-etl-jobs/curated/customers/

The table is defined as a partitioned Parquet table with:

city

as the partition column.

Glue Crawler

A Glue Crawler is not used in this project.

Instead, the table metadata is created manually and the existing S3 partitions are registered using Athena.

## 🔍 8. Register S3 Partitions

The curated data uses Hive-style partition folders:

city=Bangalore/
city=Chennai/
city=Delhi/

## After creating the Athena table, the existing partitions are registered using:

MSCK REPAIR TABLE customers;

This discovers the partition folders in:

s3://s3-to-s3-etl-jobs/curated/customers/

and registers them in the AWS Glue Data Catalog.

The command does not copy or modify the Parquet files.

Partitions can be checked using:

SHOW PARTITIONS customers;

## 🔎 9. Amazon Athena

Amazon Athena is used to query the curated Parquet data using SQL.

Athena uses the AWS Glue Data Catalog metadata to understand the table structure and partitions.

## The Athena database is:

customer_etl_db

The table is:

customers

The Athena query result location is:

s3://s3-to-s3-etl-jobs/athena-results/

Athena stores query results separately from the curated data.

## Example Athena Queries
# View customer records
SELECT *
FROM customers
LIMIT 10;


# Count customers
SELECT COUNT(*) AS total_customers
FROM customers;


# Check customers by city
SELECT
    city,
    COUNT(*) AS customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC;


# Query a specific partition
SELECT *
FROM customers
WHERE city = 'Bangalore';


# Average salary by city
SELECT
    city,
    ROUND(AVG(salary), 2) AS avg_salary
FROM customers
GROUP BY city
ORDER BY avg_salary DESC;


# Salary category distribution
SELECT
    salary_category,
    COUNT(*) AS customer_count
FROM customers
GROUP BY salary_category
ORDER BY customer_count DESC;


# Age category distribution
SELECT
    age_category,
    COUNT(*) AS customer_count
FROM customers
GROUP BY age_category
ORDER BY customer_count DESC;



## 🧪 Data Validation Queries

Additional SQL validation queries are included in:

sql/validation_queries.sql

# The queries can be used to validate:

Total customer records
Duplicate customer IDs
NULL customer IDs
NULL customer names
Invalid ages
Negative salaries
Customer count by city
Average salary by city
Salary category distribution
Age category distribution

## 📜 Glue ETL Script
The main ETL script is available here:

glue/etl_job.py

## The script handles:

Reading CSV data from S3.
Applying an explicit schema.
Cleaning the data.
Removing duplicate records.
Performing data quality checks.
Creating derived columns.
Adding the processing date.
Writing Parquet output.
Partitioning the output by city.
Logging ETL results.

## 📈 Output
The final curated dataset contains:

customer_id
name
city
age
age_category
salary
salary_category
processing_date

The output is stored as partitioned Parquet files in:

s3://s3-to-s3-etl-jobs/curated/customers/

Example:
city=Bangalore/
    part-00000-xxxx.snappy.parquet

city=Chennai/
    part-00000-xxxx.snappy.parquet
    
## 📊 Monitoring

AWS CloudWatch is used to monitor the AWS Glue ETL job.

The Glue job logs provide information about:

Job execution
Source record count
Invalid records
Final record count
Output location
Job success or failure

This helps identify data quality issues and ETL failures.

## 🔐 Security

No AWS credentials, passwords, access keys, or secret values are stored in this repository.

AWS IAM is used to provide the required permissions to the Glue job.

The Glue job uses an IAM role for access to AWS resources.

S3 input and output paths are passed through Glue job parameters rather than hardcoded in the ETL script.
