-- ======================================================
-- 🪙 CRYPTO EXCHANGE DATABASE PROJECT (FINAL FIXED 2025)
-- ======================================================

-- 1️⃣ DROP OLD DATABASE & CREATE NEW ONE
DROP DATABASE IF EXISTS crypto_exchange;
CREATE DATABASE crypto_exchange;
USE crypto_exchange;

-- ======================================================
-- 2️⃣ USER TABLE
-- ======================================================
CREATE TABLE User (
  UserID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Email VARCHAR(100) UNIQUE,
  Password VARCHAR(200) NOT NULL,
  Phone VARCHAR(15),
  KYCStatus VARCHAR(20)
);

INSERT INTO User (Name, Email, Password, Phone, KYCStatus) VALUES
('Rahul Kumar', 'rahul@gmail.com', 'pass123', '9876543210', 'Verified'),
('Ananya Gowda', 'ananya@gmail.com', 'abc123', '9123456780', 'Pending'),
('Kushal Kumar', 'kushal@gmail.com', 'qwerty', '8765432190', 'Verified'),
('Laasya R', 'laasya@gmail.com', 'sanya789', '9998887770', 'Verified'),
('Priya M', 'priya@gmail.com', 'dev456', '9786543210', 'Pending');

-- ======================================================
-- 3️⃣ CRYPTOCURRENCY TABLE
-- ======================================================
CREATE TABLE Cryptocurrency (
  CryptoID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(50) NOT NULL,
  Symbol VARCHAR(10) NOT NULL,
  BlockchainType VARCHAR(30),
  LaunchDate DATE
);

INSERT INTO Cryptocurrency (Name, Symbol, BlockchainType, LaunchDate) VALUES
('Bitcoin', 'BTC', 'Bitcoin', '2009-01-03'),
('Ethereum', 'ETH', 'Ethereum', '2015-07-30'),
('Ripple', 'XRP', 'RippleNet', '2012-06-02'),
('Cardano', 'ADA', 'Cardano', '2017-09-29'),
('Polkadot', 'DOT', 'Polkadot', '2020-08-18'),
('Dogecoin', 'DOGE', 'Dogecoin', '2013-12-06'),
('Solana', 'SOL', 'Solana', '2020-03-16'),
('Litecoin', 'LTC', 'Litecoin', '2011-10-07');

-- ======================================================
-- 4️⃣ MARKET PRICE TABLE
-- ======================================================
CREATE TABLE MarketPrice (
  PriceID INT AUTO_INCREMENT PRIMARY KEY,
  CryptoID INT,
  DateTime DATETIME DEFAULT NOW(),
  Price DECIMAL(15,2),
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID) ON DELETE CASCADE
);

INSERT INTO MarketPrice (CryptoID, DateTime, Price) VALUES
(1, NOW(), 65000.00),
(2, NOW(), 3500.00),
(3, NOW(), 0.55),
(4, NOW(), 2.50),
(5, NOW(), 6.80),
(6, NOW(), 0.20),
(7, NOW(), 120.00),
(8, NOW(), 180.00);

-- ======================================================
-- 5️⃣ WALLET TABLE
-- ======================================================
CREATE TABLE Wallet (
  UserID INT,
  CryptoID INT,
  Balance DECIMAL(15,4) DEFAULT 0.0000,
  PRIMARY KEY (UserID, CryptoID),
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID) ON DELETE CASCADE
);

INSERT INTO Wallet (UserID, CryptoID, Balance) VALUES
(1, 1, 0.50),
(1, 2, 3.25),
(2, 3, 500.00),
(3, 1, 1.20),
(3, 6, 10000.00),
(4, 2, 4.75),
(5, 4, 250.00),
(5, 5, 30.00);

-- ======================================================
-- 6️⃣ ORDERS TABLE
-- ======================================================
CREATE TABLE Orders (
  OrderID INT AUTO_INCREMENT PRIMARY KEY,
  UserID INT NOT NULL,
  CryptoID INT NOT NULL,
  OrderType ENUM('BUY', 'SELL') NOT NULL,
  Quantity DECIMAL(10,2) NOT NULL,
  Price DECIMAL(15,2) NOT NULL,
  Status VARCHAR(20) DEFAULT 'Completed',
  Timestamp DATETIME DEFAULT NOW(),
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID) ON DELETE CASCADE
);

INSERT INTO Orders (UserID, CryptoID, OrderType, Quantity, Price, Status) VALUES
(1, 1, 'BUY', 0.25, 64000, 'Completed'),
(1, 2, 'SELL', 1.00, 3400, 'Pending'),
(2, 3, 'BUY', 200.00, 0.50, 'Completed'),
(3, 6, 'BUY', 5000.00, 0.18, 'Completed'),
(4, 2, 'BUY', 1.50, 3300, 'Completed'),
(5, 5, 'SELL', 10.00, 6.50, 'Pending'),
(3, 1, 'SELL', 0.40, 66000, 'Completed'),
(5, 4, 'BUY', 100.00, 2.45, 'Completed');

-- ======================================================
-- 7️⃣ TRANSACTION TABLE
-- ======================================================
CREATE TABLE Transaction (
  TransactionID INT AUTO_INCREMENT PRIMARY KEY,
  OrderID INT,
  UserID INT,
  Amount DECIMAL(15,2),
  TransactionType VARCHAR(20),
  Timestamp DATETIME DEFAULT NOW(),
  FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);

INSERT INTO Transaction (OrderID, UserID, Amount, TransactionType) VALUES
(1, 1, 16000.00, 'Trade'),
(3, 2, 100.00, 'Trade'),
(4, 3, 900.00, 'Trade'),
(5, 4, 4950.00, 'Trade'),
(7, 3, 26400.00, 'Trade'),
(8, 5, 245.00, 'Trade');

-- ======================================================
-- 8️⃣ WATCHLIST TABLE (🛠️ FIXED)
-- ======================================================
CREATE TABLE Watchlist (
  WatchlistID INT AUTO_INCREMENT PRIMARY KEY,
  UserID INT,
  CryptoID INT,
  DateAdded DATETIME DEFAULT NOW(),
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
  FOREIGN KEY (CryptoID) REFERENCES Cryptocurrency(CryptoID) ON DELETE CASCADE
);

INSERT INTO Watchlist (UserID, CryptoID) VALUES
(1, 1),
(1, 2),
(2, 4),
(3, 6),
(4, 7),
(5, 5),
(5, 3);

-- ======================================================
-- 9️⃣ TRIGGER: AFTER ORDER INSERT
-- ======================================================
DROP TRIGGER IF EXISTS after_order_insert;
DELIMITER //

CREATE TRIGGER after_order_insert
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
  -- 🧾 Record transaction
  INSERT INTO Transaction (OrderID, UserID, Amount, TransactionType, Timestamp)
  VALUES (NEW.OrderID, NEW.UserID, (NEW.Quantity * NEW.Price), 'Trade', NOW());

  -- 💰 Wallet auto-update
  IF NEW.OrderType = 'BUY' THEN
    INSERT INTO Wallet (UserID, CryptoID, Balance)
    VALUES (NEW.UserID, NEW.CryptoID, NEW.Quantity)
    ON DUPLICATE KEY UPDATE Balance = Balance + NEW.Quantity;
  ELSEIF NEW.OrderType = 'SELL' THEN
    UPDATE Wallet
    SET Balance = Balance - NEW.Quantity
    WHERE UserID = NEW.UserID AND CryptoID = NEW.CryptoID;
  END IF;
END;
//
DELIMITER ;

-- ======================================================
-- 🔟 ADMINUSER TABLE
-- ======================================================
CREATE TABLE IF NOT EXISTS AdminUser (
  AdminID INT AUTO_INCREMENT PRIMARY KEY,
  Username VARCHAR(100) UNIQUE NOT NULL,
  Password VARCHAR(200) NOT NULL
);

INSERT INTO AdminUser (Username, Password)
VALUES ('admin', 'pass123');

-- ======================================================
-- ✅ TEST COMMANDS (optional)
-- ======================================================
SHOW TABLES;
SHOW TRIGGERS;

SELECT * FROM User;
SELECT * FROM Cryptocurrency;
SELECT * FROM Wallet;
SELECT * FROM Orders;
SELECT * FROM Transaction;
SELECT * FROM Watchlist;

-- 💹 Portfolio Calculation
SELECT 
    U.Name, 
    SUM(W.Balance * M.Price) AS Portfolio_Value_USD
FROM Wallet W
JOIN MarketPrice M ON W.CryptoID = M.CryptoID
JOIN User U ON W.UserID = U.UserID
GROUP BY U.UserID;
