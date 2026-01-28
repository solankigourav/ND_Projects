# Local Data Lake Project

This repository simulates a local "Medallion" data lake architecture. It includes a synthetic data generator for e-commerce transactions.

## 📂 Folder Structure

| Layer | Path | Description |
| :--- | :--- | :--- |
| **Raw** | `data/raw/` | Landing zone for original JSON logs. Partitioned by date. |
| **Bronze** | `data/bronze/` |  |
| **Silver** | `data/silver/` | |
| **Gold** | `data/gold/` |  |

## 📊 Dataset: Transactions

**Source:** Synthetic Python Generator (`generate_data.py`)  
**Format:** JSON Lines (New line delimited JSON)  
**Partitioning Strategy:** Hive-style partitioning by `event_date` (`/event_date=YYYY-MM-DD/`)

### Schema Definition

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `transaction_id` | String (UUID) | Unique identifier for the transaction. |
| `customer_id` | Integer | Unique identifier for the customer. |
| `customer_name` | String | Full name of the customer. |
| `product_category`| String | Category of item purchased. |
| `amount` | Float | Transaction value. |
| `payment_status` | String | Enum: COMPLETED, FAILED, PENDING. |
| `event_timestamp` | String (ISO) | Exact time of the transaction. |
| `event_date` | String (YYYY-MM-DD)| **Partition Key**. Derived from timestamp. |

## 🚀 How to Run

1. Install dependencies: `pip install pandas faker`
2. Run generator: `python generate_data.py`