import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime

# File paths for input XML, output JSON, and log file
INPUT_FILE = "data/modified_sms_v2.xml"
OUTPUT_FILE = "data/cleaned_transactions.json"
LOG_FILE = "data/unprocessed.log"

cleaned_data = []

# Function to convert amount strings like '5,000' into int 5000
def normalize_amount(amount_str):
    return int(amount_str.replace(",", "").strip())

# Function to figure out transaction type based on keywords in SMS body
def extract_transaction_type(body):
    if "You have received" in body:
        return "Incoming Money"
    elif "Your payment of" in body and "to Airtime" in body:
        return "Airtime Payment"
    elif "Your payment of" in body and "Cash Power" in body:
        return "Cash Power Payment"
    elif "Your payment of" in body:
        return "Payment to Code Holder"
    elif "*165*S*" in body and "transferred to" in body:
        return "Transfer to Mobile Number"
    elif "*113*R*" in body and "bank deposit" in body:
        return "Bank Deposit"
    elif "withdrawn" in body and "agent" in body:
        return "Withdrawal from Agent"
    elif "DIRECT PAYMENT LTD" in body:
        return "Transaction by Third Party"
    elif "one-time password" in body:
        return "OTP / Non-transactional"
    return None

# Function to get data fields out of SMS text
def parse_body(body):
    # First find what type of transaction it is
    tx_type = extract_transaction_type(body)
    if not tx_type or tx_type == "OTP / Non-transactional":
        return None

    tx = {
        "transaction_type": tx_type,
        "raw_body": body
    }

    try:
        # Find amount if it exists
        amount_match = re.search(r"([\d,]+)\s*RWF", body)
        if amount_match:
            tx["amount"] = normalize_amount(amount_match.group(1))

        # Find date and time if mentioned
        date_match = re.search(r"at\s([\d\-: ]+)", body)
        if date_match:
            raw_dt = date_match.group(1).strip()
            try:
                # Try to convert to standard datetime format
                parsed_dt = datetime.strptime(raw_dt, "%Y-%m-%d %H:%M:%S")
                tx["datetime"] = parsed_dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                # If fails, just keep raw text
                tx["datetime"] = raw_dt

        # Get transaction ID
        txid_match = re.search(r"TxId[:\s]*([0-9]+)", body)
        if txid_match:
            tx["transaction_id"] = txid_match.group(1)

        # Get balance after transaction
        balance_match = re.search(r"balance: ?([0-9,]+)\s*RWF", body)
        if balance_match:
            tx["balance"] = normalize_amount(balance_match.group(1))

        # Get receiver name or number
        receiver_match = re.search(r"to\s(.+?)(?:\.| has been completed|$)", body)
        if receiver_match:
            tx["receiver"] = receiver_match.group(1).strip()

        # Get sender name or number
        sender_match = re.search(r"from\s(.+?)(?:\.|\s|$)", body)
        if sender_match:
            tx["sender"] = sender_match.group(1).strip()

        return tx

    except Exception as err:
        log_file.write(f"[Unprocessed] {body}\nReason: {str(err)}\n\n")
        return None

# Open the log file here so we can write errors and ignored messages
with open(LOG_FILE, "w", encoding="utf-8") as log_file:
    try:
        # Load the XML file
        tree = ET.parse(INPUT_FILE)
        root = tree.getroot()

        # Loop through each SMS entry
        for sms in root.findall("sms"):
            body = sms.get("body")
            if body:
                parsed = parse_body(body)
                if parsed:
                    cleaned_data.append(parsed)
                else:
                    # Log SMS bodies we couldn't parse or ignored
                    log_file.write(f"[Ignored] {body}\n\n")

    except Exception as e:
        log_file.write(f"[Critical Error] Failed to parse XML: {str(e)}\n")

# Save all cleaned data as JSON with nice indentation
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    json.dump(cleaned_data, f_out, indent=2, ensure_ascii=False)
