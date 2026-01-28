import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# --- Configuration ---
NUM_RECORDS = 500
OUTPUT_DIR = "D:\\NeuroDrift\\ND_Projects\\Data\\raw"
START_DATE = datetime.now() - timedelta(days=10)  # Generate data for the last 10 days

fake = Faker()


def generate_synthetic_data(num_records):
    data = []
    print(f"Generating {num_records} records...")

    for _ in range(num_records):
        # Simulate an event time within the last 10 days
        event_time = fake.date_time_between(start_date=START_DATE, end_date='now')

        record = {
            "transaction_id": fake.uuid4(),
            "customer_id": fake.random_int(min=1000, max=9999),
            "customer_name": fake.name(),
            "product_category": random.choice(["Electronics", "Books", "Home", "Clothing"]),
            "amount": round(random.uniform(10.0, 1000.0), 2),
            "currency": "USD",
            "payment_status": random.choice(["COMPLETED", "FAILED", "PENDING"]),
            "event_timestamp": event_time.isoformat(),
            "event_date": event_time.strftime("%Y-%m-%d")  # This is our partition column
        }
        data.append(record)
    return pd.DataFrame(data)


def save_partitioned_data(df, base_path):
    # Group by the partition column
    unique_dates = df['event_date'].unique()

    for date in unique_dates:
        # Filter data for this specific date
        daily_df = df[df['event_date'] == date]

        # Define hive-style partition path: .../event_date=YYYY-MM-DD/
        partition_path = os.path.join(base_path, f"event_date={date}")
        os.makedirs(partition_path, exist_ok=True)

        # Save as JSON (common for raw data ingestion)
        file_name = f"data_{fake.lexify(text='????')}.json"
        full_path = os.path.join(partition_path, file_name)

        daily_df.to_json(full_path, orient='records', lines=True)
        print(f"Saved {len(daily_df)} records to {partition_path}")


# --- Execution ---
if __name__ == "__main__":
    df_transactions = generate_synthetic_data(NUM_RECORDS)
    save_partitioned_data(df_transactions, OUTPUT_DIR)
    print("\nData Lake generation complete!")