MTN MoMo SMS Dashboard

This is an enterprise-grade fullstack application developed for my coursework in **Enterprise Web Development**. The project processes and analyzes MTN Rwanda MoMo SMS transaction data delivered in XML format, stores it in a MySQL database, and presents the insights on an interactive dashboard.



 Project Overview

The MTN MoMo SMS Dashboard was built to:

1. Parse raw XML MoMo SMS messages
2. Categorize transactions (e.g., deposits, payments, airtime purchases)
3. Clean and normalize the data
4. Store structured records in a MySQL relational database
5. Serve data via a RESTful Flask API
6. Present live analytics on a web-based dashboard

The system handles over 1600 real-world SMS messages and offers dynamic charts, filters, and searchable tables.



 Project Structure


MTN-MoMo-SMS-Dashboard/
├── backend/                  # Python + Flask API
│   ├── app.py               # Main Flask server
│   ├── db_config.py         # MySQL connection logic
│   ├── models.py            # Query logic
│   ├── .env                 # Environment variables
│   └── requirements.txt     # Backend dependencies
├── data/
│   ├── modified_sms_v2.xml  # Input SMS data
│   ├── cleaned_transactions.json
│   └── unprocessed.log      # Log of ignored or malformed entries
├── frontend/                # HTML, CSS, and JavaScript dashboard
│   ├── index.html
│   ├── style.css
│   ├── app.js               # Filtering and table logic
│   └── charts.js            # Chart.js visualizations
├── parse_sms.py             # Parses XML into structured JSON
├── insert_into_mysql.py     # Inserts parsed data into MySQL
├── schema.sql               # MySQL database schema
├── AUTHORS.md               # Contributor information
└── README.md                # This file
```

---

 How to Run the Application

(i) Set Up MySQL

Create the database:

```sql
CREATE DATABASE my_momo_dashboard_db;


Import the schema:

bash
mysql -u your_mysql_user -p my_momo_dashboard_db < schema.sql


Set up environment variables in `.env`:


DB_HOST=localhost
DB_USER=my_mysql_user
DB_PASSWORD=my_mysql_password
DB_NAME=my_momo_dashboard_db




(ii) Parse and Insert Data

Run the following scripts to process the raw XML and insert cleaned data into the database:

bash
python3 parse_sms.py
python3 insert_into_mysql.py




(iii) Start the Backend Server

Navigate to the backend folder and run the Flask server:

```bash
cd backend
pip install -r requirements.txt
python3 app.py
```

The API will be accessible at:


http://localhost:5000


Example endpoints:

1. `/transactions`
2. `/summary`
3. `/transaction/<id>`



(iv) View the Frontend Dashboard

Open `frontend/index.html` in a web browser. The frontend will automatically fetch data from the Flask API and display:

1. A searchable, filterable transaction table
2. Visualizations for transaction volume, trends, and distributions
3. A detail view for individual transactions



Features

1. Real-time frontend powered by a RESTful API
2. Dynamic charts using Chart.js
3. Categorization of various transaction types
4. Responsive and minimalistic UI
5. Logging of unprocessed or malformed SMS entries



Technologies Used

1. Python
2.  Flask
3. MySQL
4. JavaScript (Vanilla)
5. Chart.js
6. HTML and CSS



Documentation

See the separately submitted `report.pdf` for the full technical breakdown, design rationale, and implementation decisions.
I have also uploaded the .zip archive project file containing all the files and source code.


Video Walkthrough

Please see the accompanying video demonstration here:
\[Insert YouTube or Google Drive link here]



Author

Ajak Bul Zachariah Chol
Enterprise Web Development — June 2025



License

This project was developed for academic purposes only and is not intended for commercial use.


