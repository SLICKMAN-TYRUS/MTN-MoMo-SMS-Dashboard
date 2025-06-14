from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from models import fetch_all_transactions, get_transaction_by_id, get_summary

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Restrict CORS to your frontend origin

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def parse_int(value, field_name):
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid integer for '{field_name}': {value}")

def validate_filters(args):
    filters = {}

    # Validate type (string, optional)
    tx_type = args.get("type")
    if tx_type:
        filters["type"] = tx_type

    # Validate min and max amounts (integers, optional)
    try:
        filters["min"] = parse_int(args.get("min"), "min")
        filters["max"] = parse_int(args.get("max"), "max")
    except ValueError as e:
        raise e

    # Validate start and end dates (strings, optional)
    # Assuming ISO format or as expected by models.py
    start = args.get("start")
    end = args.get("end")
    if start:
        filters["start"] = start
    if end:
        filters["end"] = end

    return filters

@app.route("/transactions", methods=["GET"])
def get_transactions():
    try:
        filters = validate_filters(request.args)
        logging.info(f"Filters applied: {filters}")
        data = fetch_all_transactions(filters)
        return jsonify(data)
    except ValueError as ve:
        logging.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Error fetching transactions: {e}", exc_info=True)
        return jsonify({"error": "Failed to fetch transactions"}), 500

@app.route("/transaction/<int:tx_id>", methods=["GET"])
def get_transaction(tx_id):
    try:
        data = get_transaction_by_id(tx_id)
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching transaction {tx_id}: {e}", exc_info=True)
        return jsonify({"error": "Failed to fetch transaction"}), 500

@app.route("/summary", methods=["GET"])
def get_summary_data():
    try:
        data = get_summary()
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching summary: {e}", exc_info=True)
        return jsonify({"error": "Failed to fetch summary"}), 500

# Global error handler for unexpected exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
