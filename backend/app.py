from flask import Flask, jsonify, request
from flask_cors import CORS
from models import fetch_all_transactions, get_transaction_by_id, get_summary

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route("/transactions", methods=["GET"])
def get_transactions():
    filters = {
        "type": request.args.get("type"),
        "min": request.args.get("min"),
        "max": request.args.get("max"),
        "start": request.args.get("start"),
        "end": request.args.get("end")
    }
    data = fetch_all_transactions(filters)
    return jsonify(data)

@app.route("/transaction/<int:tx_id>", methods=["GET"])
def get_transaction(tx_id):
    data = get_transaction_by_id(tx_id)
    if data:
        return jsonify(data)
    return jsonify({"error": "Transaction not found"}), 404

@app.route("/summary", methods=["GET"])
def get_summary_data():
    return jsonify(get_summary())

if __name__ == "__main__":
    app.run(debug=True)
