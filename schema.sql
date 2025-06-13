-- Create database (run this separately if needed)
CREATE DATABASE IF NOT EXISTS momo_sms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE momo_sms;

-- Table for transaction categories
CREATE TABLE IF NOT EXISTS transaction_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table for parsed transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_type_id INT,
    amount INT NOT NULL,
    datetime DATETIME,
    transaction_id VARCHAR(50),
    sender VARCHAR(100),
    receiver VARCHAR(100),
    balance INT,
    raw_body TEXT,
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(id)
);
