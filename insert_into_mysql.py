import os
import sys
import json
import mysql.connector
from datetime import datetime

# Database connection info
DB_CONFIG = {
    "host": "localhost",
    "user": "momo_dashboard_user",
    "password": "MoMoDashboardUser123!",
    "database": "my_momo_dashboard_db"
}

JSON_PATH = "data/cleaned_transactions.json"

# Load transactions from the JSON file safely
def load_transactions(json_path):
    if not os.path.exists(json_path):
        print(f"Error: JSON file {json_path} does not exist.")
        sys.exit(1)
    if os.stat(json_path).st_size == 0:
        print(f"Error: JSON file {json_path} is empty.")
        sys.exit(1)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
    if not isinstance(data, list) or len(data) == 0:
        print("No transactions found in JSON file.")
        sys.exit(1)
    return data

# Try to parse the datetime string to a format MySQL accepts
def safe_parse_datetime(dt_str):
    if not dt_str:
        return None
    # Try several datetime formats since SMS data can vary
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M"):
        try:
            dt = datetime.strptime(dt_str, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    # If none work, print a warning and store NULL in DB
    print(f"Warning: Unable to parse datetime '{dt_str}'. Storing as NULL.")
    return None

def main():
    # Get transactions from JSON file
    transactions = load_transactions(JSON_PATH)

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Get all unique transaction types from data
        transaction_types = {entry["transaction_type"] for entry in transactions}
        type_id_map = {}

        # Insert each transaction type if it doesn't exist already
        for tx_type in transaction_types:
            cursor.execute("INSERT IGNORE INTO transaction_types (name) VALUES (%s)", (tx_type,))
        conn.commit()

        # Retrieve the IDs for each transaction type we just inserted or had
        for tx_type in transaction_types:
            cursor.execute("SELECT id FROM transaction_types WHERE name = %s", (tx_type,))
            result = cursor.fetchone()
            if result:
                type_id_map[tx_type] = result[0]
            else:
                print(f"Warning: Transaction type '{tx_type}' not found after insert.")

        # Now insert all the transactions with proper foreign keys
        for tx in transactions:
            dt = safe_parse_datetime(tx.get("datetime"))
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_type_id,
                    amount,
                    datetime,
                    transaction_id,
                    sender,
                    receiver,
                    balance,
                    raw_body
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                type_id_map.get(tx.get("transaction_type")),
                tx.get("amount"),
                dt,
                tx.get("transaction_id"),
                tx.get("sender"),
                tx.get("receiver"),
                tx.get("balance"),
                tx.get("raw_body")
            ))

        conn.commit()
        print("Transaction data inserted into my_momo_dashboard_db successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Always close cursor and connection if they were opened
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
