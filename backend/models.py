from db_config import get_connection

# Fetch all transactions, optionally filtered
def fetch_all_transactions(filters=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT t.*, ty.name AS transaction_type
        FROM transactions t
        JOIN transaction_types ty ON t.transaction_type_id = ty.id
        WHERE 1=1
    """
    params = []

    if filters:
        if filters.get("type"):
            query += " AND ty.name = %s"
            params.append(filters["type"])
        if filters.get("min"):
            query += " AND t.amount >= %s"
            params.append(filters["min"])
        if filters.get("max"):
            query += " AND t.amount <= %s"
            params.append(filters["max"])
        if filters.get("start"):
            query += " AND t.datetime >= %s"
            params.append(filters["start"])
        if filters.get("end"):
            query += " AND t.datetime <= %s"
            params.append(filters["end"])

    cursor.execute(query, params)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result

# Fetch one transaction by ID
def get_transaction_by_id(tx_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT t.*, ty.name AS transaction_type
        FROM transactions t
        JOIN transaction_types ty ON t.transaction_type_id = ty.id
        WHERE t.id = %s
    """
    cursor.execute(query, (tx_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result

# Fetch summary data for charts
def get_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ty.name AS type, SUM(t.amount) AS total
        FROM transactions t
        JOIN transaction_types ty ON t.transaction_type_id = ty.id
        GROUP BY ty.name
    """)
    by_type = cursor.fetchall()

    cursor.execute("""
        SELECT DATE_FORMAT(t.datetime, '%%Y-%%m') AS month, SUM(t.amount) AS total
        FROM transactions t
        GROUP BY month
        ORDER BY month
    """)
    by_month = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "by_type": by_type,
        "by_month": by_month
    }
