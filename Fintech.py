import sqlite3
import random
import uuid
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# 1. DATABASE SETUP (Everything stays in one local folder)
def init_db():
    conn = sqlite3.connect("banking_ledger.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            acc_num TEXT PRIMARY KEY, name TEXT, balance REAL
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledger (
            tx_id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL, status TEXT
        )""")
    # Create two mock accounts for quick testing if database is new
    try:
        cursor.execute("INSERT INTO accounts VALUES ('1111111111', 'OPay User A', 50000.0)")
        cursor.execute("INSERT INTO accounts VALUES ('2222222222', 'Moniepoint User B', 1000.0)")
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Accounts already exist
    conn.close()

# 2. ASYNC MOCK PAYMENT GATEWAY (Simulates a network timeout and automated money reversal)
def process_external_transfer(tx_id, sender, amount):
    time.sleep(3) # Simulate a 3-second network delay
    conn = sqlite3.connect("banking_ledger.db")
    cursor = conn.cursor()
    
    # 15% chance the transaction fails (simulating a bank network crash)
    if random.random() < 0.15:
        cursor.execute("UPDATE ledger SET status = 'FAILED' WHERE tx_id = ?", (tx_id,))
        # REVERSAL: Give the money back to the sender because the network failed
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_num = ?", (amount, sender))
        print(f"\n[ALERT] Tx {tx_id} failed! Refunded ₦{amount} back to Account {sender}")
    else:
        cursor.execute("UPDATE ledger SET status = 'SUCCESS' WHERE tx_id = ?", (tx_id,))
        print(f"\n[SUCCESS] Tx {tx_id} cleared successfully on interbank rails!")
        
    conn.commit()
    conn.close()

# 3. HIGH-PERFORMANCE NATIVE API ROUTER
class FintechAPI(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/transfer":
            # Parse incoming transaction data
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode('utf-8'))
            sender = body['sender']
            receiver = body['receiver']
            amount = float(body['amount'])
            
            conn = sqlite3.connect("banking_ledger.db")
            cursor = conn.cursor()
            
            # Step 1: Thread-safe balance verification
            cursor.execute("SELECT balance FROM accounts WHERE acc_num = ?", (sender,))
            row = cursor.fetchone()
            
            if not row or row[0] < amount:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Insufficient wallet funds"}).encode())
                conn.close()
                return

            tx_id = str(uuid.uuid4())[:8] # Short clean ID
            
            # Step 2: Core ACID Accounting - Instantly debit sender to prevent double-spending
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE acc_num = ?", (amount, sender))
            cursor.execute("INSERT INTO ledger VALUES (?, ?, ?, ?, 'PROCESSING')", (tx_id, sender, receiver, amount))
            conn.commit()
            conn.close()
            
            # Step 3: Run the gateway switch simulation in the background so the API doesn't freeze
            threading.Thread(target=process_external_transfer, args=(tx_id, sender, amount)).start()
            
            # Respond immediately to user (Just like OPay/Moniepoint "Processing..." screen)
            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "PROCESSING",
                "transaction_id": tx_id,
                "message": f"₦{amount} debited. Awaiting external settlement gateway response."
            }).encode())

# 4. ENGINE RUNTIME
if __name__ == "__main__":
    init_db()
    print("Fintech Core Ledger Engine Online on http://127.0.0.1:8080")
    print("Pre-loaded accounts for testing: '1111111111' (₦50,000) and '2222222222' (₦1,000)")
    HTTPServer(("127.0.0.1", 8080), FintechAPI).serve_forever()
