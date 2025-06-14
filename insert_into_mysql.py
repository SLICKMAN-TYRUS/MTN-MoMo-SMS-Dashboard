import json
import mysql.connector

# Database connection settings
conn = mysql.connector.connect(
    host="localhost",
    user="momo_dashboard_user",
    password="MoMoDashboardUser123!", 
    database="my_momo_dashboard_db"
)

cursor = conn.cursor()

# Load cleaned transaction data from JSON
with open("data/cleaned_transactions.json", "r", encoding="utf-8") as f:
    transactions = json.load(f)

# Step 1: Insert transaction types into transaction_types table
transaction_types = {entry["transaction_type"] for entry in transactions}
type_id_map = {}

for tx_type in transaction_types:
    cursor.execute("INSERT IGNORE INTO transaction_types (name) VALUES (%s)", (tx_type,))
    conn.commit()
    cursor.execute("SELECT id FROM transaction_types WHERE name = %s", (tx_type,))
    type_id = cursor.fetchone()[0]
    type_id_map[tx_type] = type_id

# Step 2: Insert transactions into transactions table
for tx in transactions:
    amount = tx.get("amount")
    tx_type = tx.get("transaction_type")
    transaction_type_id = type_id_map.get(tx_type)

    # Skip if amount or transaction_type is missing
    if amount is None:
        print(f"Skipping transaction due to missing amount: {tx}")
        continue
    if transaction_type_id is None:
        print(f"Skipping transaction due to unknown transaction_type: {tx_type}")
        continue

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
        transaction_type_id,
        amount,
        tx.get("datetime"),
        tx.get("transaction_id"),
        tx.get("sender"),
        tx.get("receiver"),
        tx.get("balance"),
        tx.get("raw_body")
    ))


conn.commit()
cursor.close()
conn.close()

print("Transaction data inserted into my_momo_dashboard_db.")
