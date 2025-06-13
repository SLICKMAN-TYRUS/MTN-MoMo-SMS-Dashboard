import json
import mysql.connector

# === MySQL Connection Config ===
conn = mysql.connector.connect(
    host="localhost",
    user="momo_dashboard_user",
    password="MomoDashboardUser123!",
    database="my_momo_dashboard_user_db"
)
cursor = conn.cursor()

# === Load Cleaned Data ===
with open("data/cleaned_transactions.json", "r", encoding="utf-8") as file:
    transactions = json.load(file)

# === Insert Transaction Types First ===
type_set = {tx["transaction_type"] for tx in transactions}
type_id_map = {}

for tx_type in type_set:
    cursor.execute("INSERT IGNORE INTO transaction_types (name) VALUES (%s)", (tx_type,))
    conn.commit()
    cursor.execute("SELECT id FROM transaction_types WHERE name = %s", (tx_type,))
    type_id = cursor.fetchone()[0]
    type_id_map[tx_type] = type_id

# === Insert Transactions ===
for tx in transactions:
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
