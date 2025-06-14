# MTN MoMo SMS Dashboard

This project is an enterprise-grade fullstack application developed as part of my coursework in Enterprise Web Development. It focuses on extracting meaningful insights from mobile money transactions delivered via SMS by Rwanda’s MTN MoMo service. The application processes raw XML data, stores it in a MySQL database, and presents the information on a fully interactive dashboard.

---

## Project Overview

The MTN MoMo SMS Dashboard is designed to:
- Parse raw MoMo SMS messages provided in XML format
- Categorize transactions into meaningful types (e.g., deposits, payments, airtime purchases)
- Clean and normalize transaction data
- Store structured records in a relational database
- Expose the data via a RESTful Flask API
- Display trends and insights on a clean, user-friendly frontend dashboard

The system handles 1600+ real-world messages and offers visual reporting through dynamic charts, filters, and detailed transaction tables.

---

## Project Structure

MTN-MoMo-SMS-Dashboard/
├── backend/ # Python + Flask API
│ ├── app.py # Main Flask server
│ ├── db_config.py # MySQL connector
│ ├── models.py # Data query logic
│ ├── .env # Environment variables (credentials)
│ └── requirements.txt # Backend dependencies
├── data/ # Input + output data
│ ├── modified_sms_v2.xml # Raw SMS data
│ ├── cleaned_transactions.json
│ └── unprocessed.log # Parsing errors & ignored entries
├── frontend/ # Dashboard interface
│ ├── index.html
│ ├── style.css
│ ├── app.js # Filters + table logic
│ └── charts.js # Chart.js integration
├── parse_sms.py # XML parsing + data cleaning
├── insert_into_mysql.py # JSON → MySQL script
├── schema.sql # MySQL database schema
├── report.pdf # Project documentation
├── AUTHORS.md # Author info
└── README.md # This file

yaml
Copy
Edit

---

## How to Set It Up

### 1. MySQL Setup

- Create the database:
```sql
CREATE DATABASE my_momo_dashboard_db;
Import schema:

bash
Copy
Edit
mysql -u your_mysql_user -p my_momo_dashboard_db < schema.sql
Configure credentials in .env:

env
Copy
Edit
DB_HOST=localhost
DB_USER=my_mysql_user
DB_PASSWORD=my_password
DB_NAME=my_momo_dashboard_db
2. Parse and Insert Data
bash
Copy
Edit
python3 parse_sms.py
python3 insert_into_mysql.py
This will extract transactions from XML and insert them into the MySQL database.

3. Run the Backend Server
bash
Copy
Edit
cd backend
pip install -r requirements.txt
python3 app.py
The API will be live at:
http://localhost:5000

Test endpoints like:

/transactions

/summary

/transaction/1

4. Open the Frontend Dashboard
Open frontend/index.html directly in your browser.

It will automatically fetch data from your Flask API and render:

Filterable transaction table

Live-updating charts (Bar, Line, Pie)

Detailed info when a row is clicked

Features
Real-time filtering (type, date, amount)

Charts for volume by type, monthly trends, and distribution

Click-to-view full transaction details

Live API-powered frontend

Log of unprocessed or malformed SMS messages

Technologies Used
Python

Flask

MySQL

JavaScript (Vanilla)

Chart.js

HTML/CSS

Documentation
report.pdf — Full technical breakdown, decisions, and challenges

AUTHORS.md — Contributor details

Video Walkthrough
Watch the walkthrough here:
[Insert YouTube or Google Drive link here..............................................................................]

This video demonstrates the system architecture, functionality, and usage.

Author
Ajak Bul Zachariah Chol
Enterprise Web Development — June 2025

License
This project was developed for academic purposes only
