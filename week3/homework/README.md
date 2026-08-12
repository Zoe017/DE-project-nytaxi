# Module 3 Homework - Data Warehousing & BigQuery

## Overview

This homework focuses on working with **Google Cloud Storage (GCS)** and **BigQuery**, including:

* External tables
* Native BigQuery tables
* Columnar storage
* Partitioning
* Clustering
* Query cost optimization

The dataset contains **Yellow Taxi Trip Records from January 2024 through June 2024**.

---

## Question 1 - Counting Records

**What is the count of records for the 2024 Yellow Taxi Data?**

**Answer: 20,332,093**

Example query:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.yellow_taxi_external`;
```

---

## Question 2 - Data Read Estimation

**What is the estimated amount of data read when counting distinct `PULocationID` values on the External Table and the native BigQuery table?**

**Answer:**

* External Table: **0 MB**
* Native BigQuery Table: **155.12 MB**

Example queries:

```sql
SELECT COUNT(DISTINCT PULocationID)
FROM `PROJECT_ID.DATASET.yellow_taxi_external`;
```

```sql
SELECT COUNT(DISTINCT PULocationID)
FROM `PROJECT_ID.DATASET.yellow_taxi`;
```

---

## Question 3 - Understanding Columnar Storage

**Why are the estimated bytes different when querying one column versus two columns?**

**Answer:**

BigQuery is a columnar database, so it only scans the columns required by a query.

Querying only:

```sql
SELECT PULocationID
FROM `PROJECT_ID.DATASET.yellow_taxi`;
```

requires BigQuery to read only the `PULocationID` column.

Querying:

```sql
SELECT
    PULocationID,
    DOLocationID
FROM `PROJECT_ID.DATASET.yellow_taxi`;
```

requires BigQuery to read both columns, which increases the number of bytes processed.

---

## Question 4 - Counting Zero-Fare Trips

**How many records have a `fare_amount` of 0?**

**Answer: 8,333**

Example query:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.yellow_taxi`
WHERE fare_amount = 0;
```

---

## Question 5 - Partitioning and Clustering

**What is the best table optimization strategy if queries always filter by `tpep_dropoff_datetime` and order by `VendorID`?**

**Answer:**

**Partition by `tpep_dropoff_datetime` and cluster by `VendorID`.**

Example:

```sql
CREATE OR REPLACE TABLE `PROJECT_ID.DATASET.yellow_taxi_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `PROJECT_ID.DATASET.yellow_taxi`;
```

Partitioning reduces the amount of data scanned when filtering by date, while clustering organizes rows with similar `VendorID` values together.

---

## Question 6 - Partition Benefits

Retrieve distinct `VendorID` values for trips between March 1 and March 15, 2024.

Example query:

```sql
SELECT DISTINCT VendorID
FROM `PROJECT_ID.DATASET.yellow_taxi`
WHERE tpep_dropoff_datetime >= '2024-03-01'
  AND tpep_dropoff_datetime < '2024-03-16';
```

Using the partitioned table:

```sql
SELECT DISTINCT VendorID
FROM `PROJECT_ID.DATASET.yellow_taxi_partitioned`
WHERE tpep_dropoff_datetime >= '2024-03-01'
  AND tpep_dropoff_datetime < '2024-03-16';
```

**Answer:**

* Non-partitioned table: **310.24 MB**
* Partitioned table: **26.84 MB**

The partitioned table scans much less data because BigQuery only reads the partitions that contain records for the requested date range.

---

## Question 7 - External Table Storage

**Where is the data stored for the External Table?**

**Answer: GCP Bucket**

An external table stores only the table definition and metadata in BigQuery. The actual Parquet files remain in Google Cloud Storage.

---

## Question 8 - Clustering Best Practices

**Is it always best practice to cluster a BigQuery table?**

**Answer: False**

Clustering can improve performance for certain query patterns, but it is not automatically useful for every table.

Whether clustering is beneficial depends on factors such as:

* Table size
* Frequently filtered columns
* Query patterns
* Cardinality of the clustering columns

---

## Question 9 - Understanding Table Scans

Run:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.yellow_taxi`;
```

**Estimated bytes processed: 0 MB**

### Why?

`COUNT(*)` does not require BigQuery to scan the values stored in individual columns.

BigQuery can obtain the total row count from table metadata, so the query can return the result without reading the underlying column data.

Therefore, the estimated amount of data processed is:

**0 MB**

---

## Answers Summary

| Question | Answer                                                                          |
| -------- | ------------------------------------------------------------------------------- |
| Q1       | **20,332,093**                                                                  |
| Q2       | **0 MB External / 155.12 MB Native Table**                                      |
| Q3       | **BigQuery only scans the requested columns because it uses columnar storage**  |
| Q4       | **8,333**                                                                       |
| Q5       | **Partition by `tpep_dropoff_datetime`, cluster by `VendorID`**                 |
| Q6       | **310.24 MB non-partitioned / 26.84 MB partitioned**                            |
| Q7       | **GCP Bucket**                                                                  |
| Q8       | **False**                                                                       |
| Q9       | **0 MB — row count can be obtained from metadata without scanning column data** |

---

## Key Takeaways

Through this homework, I practiced:

* Creating external tables from data stored in GCS
* Creating native BigQuery tables
* Understanding how columnar storage affects query cost
* Comparing external and native tables
* Using partitioning to reduce scanned data
* Using clustering to optimize common query patterns
* Reading BigQuery estimated bytes before running queries
* Understanding how metadata can make some queries effectively scan 0 bytes
