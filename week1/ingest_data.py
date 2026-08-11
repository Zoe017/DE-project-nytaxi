import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5433/ny_taxi"
)
df = pd.read_parquet("green_tripdata_2025-11.parquet")

print(f"Loaded {len(df)} rows")
df.to_sql(
    name="green_taxi_trips",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=10_000,
)

print("green_taxi_trips imported successfully")
