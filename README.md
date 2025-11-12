# Crypto Exchange Database Project
A comprehensive **MySQL database system** designed to simulate a real-world cryptocurrency exchange.  
Includes **automated triggers**, **relational design**, and **Flask backend authentication** for managing users, assets, wallets, and trades.

---

## Overview
The **Crypto Exchange Database Project** manages users, crypto assets, wallets, market prices, buy/sell orders, automated transactions, and admin authentication.  

It demonstrates:
- Relational database design & normalization  
- Foreign key relationships  
- SQL analytics & triggers in MySQL  
- Integration with Flask for admin control  

**Key Components:**
- User & Admin Management (KYC & authentication)
- Cryptocurrency Data & Market Prices
- Wallet Balances & Portfolio Tracking
- Order & Transaction Management
- Automatic Transaction Logging (via trigger)
- Watchlist for tracking favorite cryptocurrencies

---

## Web Integration
The system can be integrated with a **Flask web app** for an admin dashboard and API connectivity.

### Web Application Features:
- **Dashboard:** Overview of users, wallets, and market activity  
- **User Management:** View and manage KYC and credentials  
- **Crypto Management:** Add and monitor cryptocurrency data  
- **Orders & Transactions:** Record and monitor trades  
- **Watchlist:** Track favorite cryptocurrencies  
- **Portfolio Analysis:** Calculate holdings in USD  
- **Secure Admin Login:** Access management with hashed credentials  

---

## Database Schema

### Core Tables

| Table | Description |
|--------|--------------|
| **User** | Stores user details, KYC status, and login credentials |
| **Cryptocurrency** | Contains all crypto asset details |
| **MarketPrice** | Tracks current market prices |
| **Wallet** | Maintains user crypto balances |
| **Orders** | Records buy/sell orders |
| **Transaction** | Logs all transactions (auto-triggered) |
| **Watchlist** | Tracks user’s favorite cryptocurrencies |
| **AdminUser** | Stores admin credentials for backend login |

---

### SQL Schema

#### 1️⃣ Create Database
```sql
DROP DATABASE IF EXISTS crypto_exchange;
CREATE DATABASE crypto_exchange;
USE crypto_exchange;
2️⃣ User Table
sql
Copy code
CREATE TABLE User (
  UserID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Email VARCHAR(100) UNIQUE,
  Password VARCHAR(200) NOT NULL,
  Phone VARCHAR(15),
  KYCStatus VARCHAR(20)
);
3️⃣ Cryptocurrency Table
sql
Copy code
CREATE TABLE Cryptocurrency (
  CryptoID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Symbol VARCHAR(10) NOT NULL,
  BlockchainType VARCHAR(30),
  LaunchDate DATE
);
4️⃣ Market Price Table
sql
Copy code
CREATE TABLE MarketPrice (
  PriceID INT AUTO_INCREMENT PRIMARY KEY,
  CryptoID INT,
  DateTime DATETIME,
  Price DECIMAL(15,2),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
5️⃣ Wallet Table
sql
Copy code
CREATE TABLE Wallet (
  UserID INT,
  CryptoID INT,
  Balance DECIMAL(15,4),
  PRIMARY KEY (UserID, CryptoID),
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
6️⃣ Orders Table
sql
Copy code
CREATE TABLE Orders (
  OrderID INT AUTO_INCREMENT PRIMARY KEY,
  UserID INT,
  CryptoID INT,
  OrderType VARCHAR(10),
  Quantity DECIMAL(10,2),
  Price DECIMAL(15,2),
  Status VARCHAR(20),
  Timestamp DATETIME,
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
7️⃣ Transaction Table
sql
Copy code
CREATE TABLE Transaction (
  TransactionID INT AUTO_INCREMENT PRIMARY KEY,
  OrderID INT,
  UserID INT,
  Amount DECIMAL(15,2),
  TransactionType VARCHAR(20),
  Timestamp DATETIME,
  FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);
8️⃣ Watchlist Table
sql
Copy code
CREATE TABLE Watchlist (
  WatchlistID INT AUTO_INCREMENT PRIMARY KEY,
  UserID INT,
  CryptoID INT,
  DateAdded DATE,
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
9️⃣ Trigger – Auto Transaction Log
sql
Copy code
DROP TRIGGER IF EXISTS after_order_insert;
DELIMITER //
CREATE TRIGGER after_order_insert
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
  INSERT INTO Transaction (OrderID, UserID, Amount, TransactionType, Timestamp)
  VALUES (NEW.OrderID, NEW.UserID, (NEW.Quantity * NEW.Price), 'Trade', NOW());
END;
//
DELIMITER ;
🔐 10️⃣ Admin Table
sql
Copy code
CREATE TABLE IF NOT EXISTS AdminUser (
  AdminID INT AUTO_INCREMENT PRIMARY KEY,
  Username VARCHAR(100) UNIQUE NOT NULL,
  Password VARCHAR(200) NOT NULL
);

INSERT INTO AdminUser (Username, Password)
VALUES ('admin', '$pbkdf2:sha256:600000$UFXvGKoLmDPCdBrT$4d84b28f78c5b93a6d98a6d9cf7898bdbf74b440ee0a1cb0f66bfcdf5ad1b8df');
 Quick Setup
 Prerequisites
MySQL 8.0 or higher

MySQL Workbench or CLI

Flask (optional for web interface)

Python 3.10+ and pip

Installation Steps
Clone or download the repository:

bash
Copy code
git clone https://github.com/your-username/crypto-exchange-db.git
cd crypto-exchange-db
Create and initialize the database:

bash
Copy code
mysql -u root -p < database_schema.sql
Verify setup:

bash
Copy code
mysql -u root -p -e "USE crypto_exchange; SHOW TABLES; SHOW TRIGGERS;"
(Optional) Run Flask backend:

bash
Copy code
pip install -r requirements.txt
python app.py
Visit web app:
http://localhost:5000

📁 File Structure
bash
Copy code
crypto-exchange-db/
├── README.md                  # Project documentation
├── database_schema.sql        # All database tables and triggers
├── app.py                     # Flask backend (optional)
├── requirements.txt            # Dependencies
├── templates/                 # HTML templates for admin UI
│   ├── login.html
│   ├── dashboard.html
│   └── portfolio.html
└── sample_queries.sql         # Verification and test queries
 Key Features & Triggers
Data Validation & Automation
Automatic Transaction Logging: Trigger inserts transaction records after new orders

Portfolio Calculation: Computes USD value per user

KYC Validation: Ensures verified users only

Watchlist Tracking: Tracks favorite cryptocurrencies

Business Logic & Analytics
Order-book management and trade history

Join queries for user portfolio computation

Aggregated data for admin reports

Enforced foreign key integrity

 Sample Portfolio Query
sql
Copy code
SELECT 
    U.Name, 
    SUM(W.Balance * M.Price) AS Portfolio_Value_USD
FROM Wallet W
JOIN MarketPrice M ON W.CryptoID = M.CryptoID
JOIN User U ON W.UserID = U.UserID
GROUP BY U.UserID;
🔧 Technology Stack
Layer	Technology
Database	MySQL 8.x
Backend (Optional)	Flask
Frontend (Optional)	HTML5, Bootstrap
Tools	MySQL Workbench, VS Code

🧪 Validation & Testing
After setup, run:

sql
Copy code
SHOW TABLES;
SHOW TRIGGERS;
SELECT * FROM Transaction;
Expected Output:
✅ Tables created successfully
✅ Trigger after_order_insert logs new transactions
✅ Admin user seeded

👥 Team Members
Name	Role
Kushal Kumar - Database Design, Integration & Backend
Laasya R - Data Insertion, SQL Queries & Frontend

Example Outputs
Tables:
pgsql
Copy code
User, Cryptocurrency, MarketPrice, Wallet, Orders, Transaction, Watchlist, AdminUser
Trigger:
sql
Copy code
after_order_insert | INSERT | Orders | AFTER | INSERT INTO Transaction ...
Portfolio Query Result:
Name	Portfolio_Value_USD
Rahul Kumar	228,500.00
Ananya Gowda	275.00
Kushal Kumar	9,600.00
Laasya R	15,825.00
Priya M	1,950.00

License
This project is open-source for academic and learning purposes.
You may reuse or modify it for educational projects.
