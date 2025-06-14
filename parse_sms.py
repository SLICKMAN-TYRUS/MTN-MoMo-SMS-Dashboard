import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime

INPUT_FILE = "data/modified_sms_v2.xml"
OUTPUT_FILE = "data/cleaned_transactions.json"
LOG_FILE = "data/unprocessed.log"

cleaned_data = []

def normalize_amount(amount_str):
    return int(amount_str.replace(",", "").strip())

def extract_transaction_type(body):
    body_lower = body.lower()
    if "you have received" in body_lower:
        return "Incoming Money"
    elif "your payment of" in body_lower and "airtime" in body_lower:
        return "Airtime Payment"
    elif "your payment of" in body_lower and "cash power" in body_lower:
        return "Cash Power Payment"
    elif "your payment of" in body_lower:
        return "General Payment"
    elif "withdrawn" in body_lower and "agent" in body_lower:
        return "Agent Withdrawal"
    elif "one-time password" in body_lower:
        return "OTP / Non-transactional"
    return None

def parse_body(body):
    tx_type = extract_transaction_type(body)
    if not tx_type or tx_type == "OTP / Non-transactional":
        return None

    tx = {
        "transaction_type": tx_type,
        "raw_body": body
    }

    try:
        # Amount
        amount_match = re.search(r"received\s([\d,]+)\s*RWF", body)
        if amount_match:
            tx["amount"] = normalize_amount(amount_match.group(1))

        # Date and Time
        date_match = re.search(r"at\s(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        if date_match:
            raw_dt = date_match.group(1).strip()
            try:
                dt = datetime.strptime(raw_dt, "%Y-%m-%d %H:%M:%S")
                tx["datetime"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                tx["datetime"] = raw_dt

        # Sender
        sender_match = re.search(r"from\s(.+?)\s\(", body)
        if sender_match:
            tx["sender"] = sender_match.group(1).strip()

        # Balance
        balance_match = re.search(r"balance[:]? ?([\d,]+)\s*RWF", body)
        if balance_match:
            tx["balance"] = normalize_amount(balance_match.group(1))

        # Transaction ID
        txid_match = re.search(r"(TxId|Financial Transaction Id)[:\s]*([0-9]+)", body)
        if txid_match:
            tx["transaction_id"] = txid_match.group(2)

        return tx

    except Exception as err:
        return None

# Start processing
with open(LOG_FILE, "w", encoding="utf-8") as log_file:
    try:
        tree = ET.parse(INPUT_FILE)
        root = tree.getroot()
        sms_list = root.findall(".//sms")

        print(f"Found {len(sms_list)} SMS messages")

        for sms in sms_list:
            body = sms.get("body")
            if not body:
                continue
            parsed = parse_body(body)
            if parsed:
                cleaned_data.append(parsed)
                print("Parsed:", parsed)
            else:
                log_file.write(f"[Ignored] {body}\n\n")

    except Exception as e:
        log_file.write(f"[Critical Error] Failed to parse XML: {str(e)}\n")
        print("Critical error:", str(e))

# Save output
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(cleaned_data, out, indent=2, ensure_ascii=False)

print(f"\nFinished. Parsed: {len(cleaned_data)} entries.")
