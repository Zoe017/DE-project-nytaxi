# Week 1: Docker and PostgreSQL

This folder contains the Week 1 environment and ingestion script for the NYC Taxi data engineering project.

## Contents

- `docker-compose.yaml`: starts PostgreSQL and pgAdmin.
- `ingest_data.py`: loads the November 2025 Green Taxi parquet file into PostgreSQL.
- `homework/`: Week 1 homework notes and answers.

## Run locally

From this directory:

```bash
docker compose up -d
python ingest_data.py
```

The ingestion script expects `green_tripdata_2025-11.parquet` in this directory.
