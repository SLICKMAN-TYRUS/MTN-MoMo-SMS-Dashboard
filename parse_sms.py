import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime

# === File Paths ===
INPUT_FILE = "data/modified_sms_v2.xml"
OUTPUT_FILE = "data/cleaned_transactions.json"
LOG_FILE = "data/unprocessed.log"

# === Storage Containers ===
cleaned_data = []
log_file = open(LOG_FILE, "w", encoding="utf-8")

def normalize_amount(amount_str):
    """
    Converts '5,000' or '1000' to integer 5000 or 1000
    """
    return int(amount_str.replace(",", "").strip())

def extract_transaction_type(body):
    """
    Determines transaction type based on key phrases.
    """
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

def parse_body(body):
    """
    Extracts structured data from raw SMS content.
    """
    tx_type = extract_transaction_type(body)
    if not tx_type or tx_type == "OTP / Non-transactional":
        return None

    tx = {
        "transaction_type": tx_type,
        "raw_body": body
    }

    try:
        # Amount
        amount_match = re.search(r"([\d,]+)\s*RWF", body)
        if amount_match:
            tx["amount"] = normalize_amount(amount_match.group(1))

        # Datetime (if present)
        date_match = re.search(r"at\s([\d\-: ]+)", body)
        if date_match:
            tx["datetime"] = date_match.group(1).strip()

        # Transaction ID
        txid_match = re.search(r"TxId[:\s]*([0-9]+)", body)
        if txid_match:
            tx["transaction_id"] = txid_match.group(1)

        # Balance
        balance_match = re.search(r"balance: ?([0-9,]+)\s*RWF", body)
        if balance_match:
            tx["balance"] = normalize_amount(balance_match.group(1))

        # Receiver
        receiver_match = re.search(r"to\s(.+?)(?:[\.\d]|has been completed)", body)
        if receiver_match:
            tx["receiver"] = receiver_match.group(1).strip()

        # Sender
        sender_match = re.search(r"from\s(.+?)\s", body)
        if sender_match:
            tx["sender"] = sender_match.group(1).strip()

        return tx

    except Exception as err:
        log_file.write(f"[Unprocessed] {body}\nReason: {str(err)}\n\n")
        return None

# === Begin XML Parsing ===
try:
    tree = ET.parse(INPUT_FILE)
    root = tree.getroot()

    for sms in root.findall("sms"):
        body = sms.get("body")
        if body:
            parsed = parse_body(body)
            if parsed:
                cleaned_data.append(parsed)
            else:
                log_file.write(f"[Ignored] {body}\n\n")

except Exception as e:
    log_file.write(f"[Critical Error] Failed to parse XML: {str(e)}\n")

# === Output Cleaned Data ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    json.dump(cleaned_data, f_out, indent=2, ensure_ascii=False)

log_file.close()
