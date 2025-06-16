from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'momo_dashboard_user',
    'password': 'MoMoDashboardUser123!',
    'database': 'my_momo_dashboard_db'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        app.logger.error(f"MySQL connection error: {e}")
        return None

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the MTN MoMo SMS Dashboard API 🎉'})

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Could not connect to the database'}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM transactions ORDER BY transaction_date DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify(rows)
    except Error as e:
        app.logger.error(f"MySQL query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        cursor.close()
        connection.close()

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
