# Module 2 Homework - Workflow Orchestration

## Overview

This homework focuses on workflow orchestration using Kestra.

The main tasks include:

- Processing NYC Yellow and Green Taxi data
- Extending the existing pipeline to include 2021 data
- Using Kestra backfill for historical data
- Loading data into Google Cloud Storage and BigQuery
- Verifying results using BigQuery

---

## Assignment

The existing Kestra taxi pipeline was extended to process data for 2021.

The available data range is:

- January 2021
- February 2021
- March 2021
- April 2021
- May 2021
- June 2021
- July 2021

The backfill was performed for both:

- Yellow Taxi
- Green Taxi

Backfill range:

```text
2021-01-01 to 2021-07-31
```

The data pipeline follows this structure:

```text
NYC Taxi Dataset
        ↓
      Kestra
        ↓
     Extract
        ↓
 Google Cloud Storage
        ↓
     BigQuery
```

The Kestra flow used for this assignment is located in:

```text
../flows/
```

---

# Quiz Answers

## Question 1

**Within the execution for Yellow Taxi data for December 2020, what is the uncompressed file size?**

Answer:

**134.5 MiB**

The file is:

```text
yellow_tripdata_2020-12.csv
```

---

## Question 2

**What is the rendered value of the variable `file` when:**

```text
taxi = green
year = 2020
month = 04
```

The Kestra variable is defined as:

```yaml
file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

After rendering:

```text
green_tripdata_2020-04.csv
```

Answer:

**green_tripdata_2020-04.csv**

---

## Question 3

**How many rows are there for the Yellow Taxi data for all CSV files in 2020?**

Answer:

**24,648,499**

Verification query:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.yellow_tripdata`
WHERE filename LIKE 'yellow_tripdata_2020-%';
```

---

## Question 4

**How many rows are there for the Green Taxi data for all CSV files in 2020?**

Answer:

**1,734,051**

Verification query:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.green_tripdata`
WHERE filename LIKE 'green_tripdata_2020-%';
```

---

## Question 5

**How many rows are there for the Yellow Taxi data for March 2021?**

Answer:

**1,925,152**

Verification query:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.yellow_tripdata`
WHERE filename = 'yellow_tripdata_2021-03.csv';
```

Alternatively, the monthly table can be queried directly:

```sql
SELECT COUNT(*)
FROM `PROJECT_ID.DATASET.yellow_tripdata_2021_03`;
```

---

## Question 6

**How would you configure the timezone to New York in a Kestra Schedule trigger?**

Answer:

```yaml
timezone: America/New_York
```

Example:

```yaml
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: America/New_York
    inputs:
      taxi: green
```

Using `America/New_York` allows the schedule to correctly handle both EST and EDT.

---

# Answers Summary

| Question | Answer |
|---|---|
| Q1 | 134.5 MiB |
| Q2 | `green_tripdata_2020-04.csv` |
| Q3 | 24,648,499 |
| Q4 | 1,734,051 |
| Q5 | 1,925,152 |
| Q6 | `America/New_York` |

---

# 2021 Backfill

The scheduled Kestra flow was used to backfill NYC Taxi data for 2021.

## Yellow Taxi

```text
Start: 2021-01-01
End:   2021-07-31
```

Months processed:

```text
2021-01
2021-02
2021-03
2021-04
2021-05
2021-06
2021-07
```

## Green Taxi

```text
Start: 2021-01-01
End:   2021-07-31
```

Months processed:

```text
2021-01
2021-02
2021-03
2021-04
2021-05
2021-06
2021-07
```

In total:

```text
7 Yellow Taxi months
+
7 Green Taxi months
=
14 monthly datasets
```

---

# Verification in BigQuery

The loaded data can be checked by grouping rows by source filename.

Example for Yellow Taxi:

```sql
SELECT
    filename,
    COUNT(*) AS row_count
FROM `PROJECT_ID.DATASET.yellow_tripdata`
WHERE filename LIKE 'yellow_tripdata_2021-%'
GROUP BY filename
ORDER BY filename;
```

Example for Green Taxi:

```sql
SELECT
    filename,
    COUNT(*) AS row_count
FROM `PROJECT_ID.DATASET.green_tripdata`
WHERE filename LIKE 'green_tripdata_2021-%'
GROUP BY filename
ORDER BY filename;
```

These queries make it possible to confirm that all seven months were successfully loaded.

---

# Kestra Flows

The Kestra YAML files used for this module are stored in:

```text
week2/flows/
```

Example structure:

```text
week2/
├── README.md
├── flows/
│   ├── 08_gcp_taxi.yaml
│   └── 09_gcp_taxi_scheduled.yaml
│
└── homework/
    └── README.md
```

---

# Key Takeaways

Through this homework I practiced:

- Creating and running Kestra workflows
- Using Kestra inputs and variables
- Rendering dynamic filenames
- Scheduling data pipelines
- Using backfill to process historical data
- Uploading files to Google Cloud Storage
- Loading data into BigQuery
- Querying and validating pipeline results with SQL
- Configuring schedule timezones
