from flask import Flask, render_template

app = Flask(__name__)

# ------------------------------
# TEMP MOCK DATA (for UI testing)
# ------------------------------

cryptos = [
    {"Name": "Bitcoin", "Symbol": "BTC", "BlockchainType": "Bitcoin", "LaunchDate": "2009-01-03"},
    {"Name": "Ethereum", "Symbol": "ETH", "BlockchainType": "Ethereum", "LaunchDate": "2015-07-30"},
    {"Name": "Solana", "Symbol": "SOL", "BlockchainType": "Solana", "LaunchDate": "2020-03-16"}
]

users = [
    {"UserID": 1, "Name": "Rahul Kumar", "KYCStatus": "Verified"},
    {"UserID": 2, "Name": "Ananya Gowda", "KYCStatus": "Pending"},
    {"UserID": 3, "Name": "Laasya R", "KYCStatus": "Verified"}
]

wallets = [
    {"Crypto": "Bitcoin", "Balance": 0.45},
    {"Crypto": "Ethereum", "Balance": 3.25},
    {"Crypto": "Solana", "Balance": 12.75}
]

transactions = [
    {"Type": "Buy", "Amount": 15000, "Timestamp": "2025-11-05 12:30"},
    {"Type": "Sell", "Amount": 22000, "Timestamp": "2025-11-06 10:15"}
]


# ------------------------------
# MOCK ROUTES (temporary)
# ------------------------------

@app.route('/')
def index():
    return render_template('index.html', cryptos=cryptos)

@app.route('/users')
def users():
    return render_template('users.html', users=users)

@app.route('/user/1')
def user_dashboard():
    user = users[0]
    return render_template('user/dashboard.html', user=user, wallet=wallets, transactions=transactions)


@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html',
                           users_count=len(users),
                           orders_count=12,
                           cryptos_count=len(cryptos))
@app.route('/wallet')
def wallet_page():
    # Temporary mock data for now
    wallets = [
        {"Crypto": "Bitcoin", "Balance": 0.45},
        {"Crypto": "Ethereum", "Balance": 3.25},
        {"Crypto": "Solana", "Balance": 12.75}
    ]
    return render_template('user/wallet.html', wallet=wallets)



if __name__ == '__main__':
    app.run(debug=True)
