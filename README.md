Crypto Exchange Database Project
Overview
The Crypto Exchange Database Project is a structured relational database system designed to simulate a real-world cryptocurrency exchange.

It manages users, crypto assets, wallets, market prices, buy/sell orders, automated transactions via triggers, and admin authentication for monitoring activity.
This project demonstrates database design, normalization, foreign keys, triggers, and SQL analytics in MySQL.
Features
User Management — Stores KYC, credentials, and profile info
Cryptocurrency Data — Includes major crypto coins with blockchain details
Wallets — Tracks user holdings and balances
Orders — Handles buy/sell transactions with timestamps
Automatic Transactions — Trigger automatically logs transactions for each order
Watchlist — Lets users track favorite cryptocurrencies
Admin Login — For Flask or backend authentication
Portfolio Value Query — Calculates total holdings in USD for each user
Database Setup
1. Create and Use Database

DROP DATABASE IF EXISTS crypto_exchange;CREATE DATABASE crypto_exchange;
USE crypto_exchange;
2. User Table
Stores user information including KYC status.


CREATE TABLE User (
  UserID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Email VARCHAR(100) UNIQUE,
  Password VARCHAR(200) NOT NULL,
  Phone VARCHAR(15),
  KYCStatus VARCHAR(20)
);
3. Cryptocurrency Table
Stores details of available cryptocurrencies.


CREATE TABLE Cryptocurrency (
  CryptoID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Symbol VARCHAR(10) NOT NULL,
  BlockchainType VARCHAR(30),
  LaunchDate DATE
);
4. Market Price Table
Tracks the current market price for each crypto.


CREATE TABLE MarketPrice (
  PriceID INT AUTO_INCREMENT PRIMARY KEY,
  CryptoID INT,
  DateTime DATETIME,
  Price DECIMAL(15,2),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
5. Wallet Table
Links users to their crypto balances.


CREATE TABLE Wallet (
  UserID INT,
  CryptoID INT,
  Balance DECIMAL(15,4),
  PRIMARY KEY (UserID, CryptoID),
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
6. Orders Table
Stores buy/sell orders with quantity, price, and status.


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
7. Transaction Table
Stores all financial transactions (auto-populated via trigger).


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
8. Watchlist Table
Tracks cryptos users want to monitor.


CREATE TABLE Watchlist (
  WatchlistID INT AUTO_INCREMENT PRIMARY KEY,
  UserID INT,
  CryptoID INT,
  DateAdded DATE,
  FOREIGN KEY (UserID) REFERENCES User(UserID),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID)
);
9. Trigger (Automatic Transaction Log)
Automatically logs a transaction whenever a new order is created.


DROP TRIGGER IF EXISTS after_order_insert;
DELIMITER //CREATE TRIGGER after_order_insert
AFTER INSERT ON OrdersFOR EACH ROWBEGIN
  INSERT INTO Transaction (OrderID, UserID, Amount, TransactionType, Timestamp)
  VALUES (NEW.OrderID, NEW.UserID, (NEW.Quantity * NEW.Price), 'Trade', NOW());END;//
DELIMITER ;
10. Admin Table (for Flask Admin Login)
For secure backend access to admin dashboards.


CREATE TABLE IF NOT EXISTS AdminUser (
  AdminID INT AUTO_INCREMENT PRIMARY KEY,
  Username VARCHAR(100) UNIQUE NOT NULL,
  Password VARCHAR(200) NOT NULL
);INSERT INTO AdminUser (Username, Password)VALUES ('admin', '$pbkdf2:sha256:600000$UFXvGKoLmDPCdBrT$4d84b28f78c5b93a6d98a6d9cf7898bdbf74b440ee0a1cb0f66bfcdf5ad1b8df');
Verification Commands
Show all tables

SHOW TABLES;
Check trigger

SHOW TRIGGERS;
View sample data

SELECT * FROM User;SELECT * FROM Cryptocurrency;SELECT * FROM Wallet;SELECT * FROM Orders;SELECT * FROM Transaction;SELECT * FROM Watchlist;SELECT * FROM AdminUser;
Portfolio Value Query
Calculate total USD value of each user’s portfolio.


SELECT 
    U.Name, 
    SUM(W.Balance * M.Price) AS Portfolio_Value_USDFROM Wallet WJOIN MarketPrice M ON W.CryptoID = M.CryptoIDJOIN User U ON W.UserID = U.UserIDGROUP BY U.UserID;
Key Concepts Used
ConceptDescriptionPrimary KeyEnsures unique identification of each recordForeign KeyLinks data across tablesTriggerAutomates actions on insertJoinsCombine data across multiple tablesNormalizationAvoids data redundancyAuto IncrementAutomatically generates unique IDs
Tools Used
MySQL Server 8.x
MySQL Workbench
Flask (optional) — for Admin UI integration
SQL Script (.sql) file for easy import
How to Run
Open MySQL Workbench
Create a new connection and open a New Query Tab
Paste the entire SQL script (or import the .sql file)
Click on the Execute All button
Run verification queries to confirm successful setup

Team Members:
Kushal Kumar - Database Design, Integration and backend
Laasya R - Data Insertion, SQL Queries and frontend

Output Samples
Example: Tables

SHOW TABLES;User
Cryptocurrency
MarketPrice
Wallet
OrdersTransaction
Watchlist
AdminUser
Example: Trigger Created

SHOW TRIGGERS;

after_order_insert | INSERT | Orders | AFTER | INSERT INTO Transaction ...
Example: Portfolio Query Result
NamePortfolio_Value_USDRahul Kumar228,500.00Ananya Gowda275.00Kushal Kumar9600.00Laasya R15,825.00Priya M1,950.00

License
This project is open-source for academic and learning purposes.

You may reuse or modify the SQL schema for educational projects.

