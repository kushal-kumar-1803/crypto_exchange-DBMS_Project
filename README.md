# Virtual Crypto Exchange Database System
A **Flask + MySQL-based web application** that simulates a real-world cryptocurrency exchange.  
It provides secure user and admin management, trading operations, live portfolio calculations, and automated transaction triggers for realistic exchange behavior.

---

## 📋 Overview
The **Crypto Exchange Database System** integrates a **MySQL relational database** with a **Flask backend** to handle:
- User registration, authentication, and KYC verification  
- Buy/sell order management with automatic transaction logging  
- Wallet and portfolio tracking  
- Cryptocurrency data and real-time pricing  
- Admin monitoring and analytics dashboard  

**Key Highlights**
- Full relational schema with foreign keys and triggers  
- Automated transaction logging using MySQL triggers  
- Secure hashed admin login credentials  
- Flask backend with modular routes and templates  
- Portfolio computation in USD value per user  

---

## 🌐 Web Application
The Flask web app provides a clean, modular structure for managing exchange operations.

### Key Features
- **Dashboard:** Displays key stats, users, wallets, and trades  
- **User Management:** Registration, login, KYC, wallet balance view  
- **Admin Panel:** Transaction and market monitoring tools  
- **Crypto Management:** Manage coins and update market prices  
- **Trading:** Place buy/sell orders with instant wallet updates  
- **Triggers:** Automatically insert transaction records upon order creation  
- **Responsive Design:** Built with clean Bootstrap templates  

### Technology Stack
| Layer | Technology |
|-------|-------------|
| **Backend** | Flask (Python) |
| **Database** | MySQL 8.0+ |
| **Frontend** | HTML5, CSS3, JS, Bootstrap |
| **ORM / DB Access** | Flask-SQLAlchemy or MySQL Connector |
| **Environment Config** | `.env.example` |

---

## 🗄️ Database Schema

### Core Tables
| Table | Description |
|--------|--------------|
| **User** | Stores user credentials, phone, and KYC status |
| **Cryptocurrency** | Lists supported cryptocurrencies and blockchain info |
| **MarketPrice** | Tracks current prices of each coin |
| **Wallet** | Links users with their crypto balances |
| **Orders** | Stores buy/sell orders |
| **Transaction** | Automatically logs each trade |
| **Watchlist** | Tracks user-selected cryptos |
| **AdminUser** | Stores admin login credentials |

### Triggers
- **`after_order_insert`** — Automatically creates a transaction record when a new order is placed.

---

## 🚀 Quick Setup

### 🧩 Prerequisites
- Python 3.10 or above  
- MySQL 8.0+  
- MySQL Workbench or CLI  
- Flask and pip environment  

---

### ⚙️ Installation Steps

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/crypto-exchange-db.git
cd crypto-exchange-db
2️⃣ Set Up Virtual Environment
bash
Copy code
python -m venv .venv
source .venv/Scripts/activate   # for Windows PowerShell
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure Database Connection
Rename .env.example → .env and update credentials:

ini
Copy code
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=crypto_exchange
5️⃣ Import Database Schema
bash
Copy code
mysql -u root -p < database/crypto_exchange_final_fixed.sql
6️⃣ Run the Application
bash
Copy code
python app.py
7️⃣ Access Web Interface
Open your browser:
👉 http://localhost:5000

📁 File Structure
graphql
Copy code
DBMS_PROJECT_BACKUP/
├── database/
│   └── crypto_exchange_final_fixed.sql     # MySQL schema with tables & triggers
│
├── models/                                 # ORM models for database entities
│   ├── __init__.py
│   ├── admin_models.py
│   ├── crypto_models.py
│   └── user_models.py
│
├── routes/                                 # Flask route controllers
│   ├── __init__.py
│   ├── admin_routes.py
│   ├── public_routes.py
│   └── user_routes.py
│
├── static/                                 # Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── user_list.html
│   ├── admin/
│   └── user/
│
├── app.py                                  # Main Flask app entry point
├── config.py                               # Configuration and DB setup
├── extensions.py                           # Flask extensions initialization
├── db_operations.py                        # SQL and helper functions
├── requirements.txt                        # Python dependencies
├── .env.example                            # Environment config template
├── .gitignore                              # Files ignored in Git
└── README.md                               # Project documentation

🧩 Core SQL Schema
Example Table: User
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
Example Trigger
sql
Copy code
CREATE TRIGGER after_order_insert
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
  INSERT INTO Transaction (OrderID, UserID, Amount, TransactionType, Timestamp)
  VALUES (NEW.OrderID, NEW.UserID, (NEW.Quantity * NEW.Price), 'Trade', NOW());
END;
🧮 Portfolio Value Query
Calculate each user's total crypto value in USD:

sql
Copy code
SELECT 
    U.Name, 
    SUM(W.Balance * M.Price) AS Portfolio_Value_USD
FROM Wallet W
JOIN MarketPrice M ON W.CryptoID = M.CryptoID
JOIN User U ON W.UserID = U.UserID
GROUP BY U.UserID;
🔐 Admin Credentials (Default)
Username	Password
admin	(hashed) $pbkdf2:sha256:600000$UFXvGKoLmDPCdBrT...

Use Flask’s generate_password_hash() to update credentials if needed.

🧠 Key Features & Triggers
⚙️ Automation
Transaction auto-logging on each order

Portfolio recalculations based on latest market prices

KYC verification enforcement

💡 Business Logic
Secure user authentication

Multi-crypto wallet linking

Real-time portfolio aggregation

Normalized data schema with foreign keys

🧪 Testing and Verification
Run these commands in MySQL:

sql
Copy code
SHOW TABLES;
SHOW TRIGGERS;
SELECT * FROM Transaction;
Expected Output:
✅ Tables successfully created
✅ Trigger after_order_insert active
✅ Admin login record inserted

👥 Team Members
Name	Role
Kushal Kumar - Database Design, Integration & Backend
Laasya R - Data Insertion, SQL Queries & Frontend

🧾 Example Outputs
Trigger Verification
sql
Copy code
SHOW TRIGGERS;
after_order_insert | INSERT | Orders | AFTER | INSERT INTO Transaction ...
Portfolio Query Result
Name	Portfolio_Value_USD
Rahul Kumar	228,500.00
Ananya Gowda	275.00
Kushal Kumar	9,600.00
Laasya R	15,825.00
Priya M	1,950.00

⚖️ License
This project is open-source for academic and learning purposes.
You may reuse or modify it for educational projects.
