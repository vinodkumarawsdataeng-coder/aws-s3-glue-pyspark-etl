# Project Overview

## Customer Data ETL Pipeline

This project demonstrates a simple AWS data engineering pipeline that
takes customer data from Amazon S3, processes it using AWS Glue and
PySpark, and stores the transformed data back in S3 in Parquet format.

## Data Flow

```text
CSV File
   |
   v
Amazon S3 - Raw Layer
   |
   v
AWS Glue + PySpark
   |
   |-- Data Cleaning
   |-- Duplicate Removal
   |-- Data Validation
   |-- Transformations
   |
   v
Amazon S3 - Curated Layer
   |
   v
Parquet Files

## Input Data

The input file contains customer information:

- Customer ID
- Customer Name
- City
- Age
- Salary

The sample data is available in the `data` folder.

## Processing Steps

The Glue job performs the following steps:

1. Reads the CSV file from Amazon S3.
2. Applies a defined schema to the data.
3. Removes records with missing required values.
4. Removes duplicate customer records.
5. Cleans the name and city columns.
6. Creates salary categories.
7. Creates age categories.
8. Adds the processing date.
9. Performs basic data quality checks.
10. Writes the processed data to S3 in Parquet format.
11. Partitions the output by city.

## Output

The processed data is stored in the S3 curated layer as Parquet files.

The output is partitioned by city:

```text
curated/customers/
    city=Bangalore/
    city=Chennai/
    city=Delhi/
    city=Hyderabad/
    city=Mumbai/

## AWS Services Used

- Amazon S3
- AWS Glue
- PySpark
- IAM
- Amazon CloudWatch

**Project Structure**
aws-s3-glue-pyspark-etl/
│
├── data/
│   └── customers.csv
│
├── glue/
│   └── etl_job.py
│
├── sql/
│   └── validation_queries.sql
│
├── docs/
│   └── project-overview.md
│
└── README.md


## Purpose

This project demonstrates a small AWS-based ETL pipeline using
Amazon S3, AWS Glue, and PySpark.

It covers common data engineering tasks such as:

- Reading CSV data from S3
- Data cleaning
- Removing duplicate records
- Data quality checks
- Data transformation
- Writing data in Parquet format
- Partitioning data by city

The project is built as a simple example of how raw data can be
processed and converted into a curated dataset for further analysis.
