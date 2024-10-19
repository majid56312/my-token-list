import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('urialex.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS currencies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    symbol TEXT
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    currency_id INTEGER,
                    amount REAL,
                    price REAL,
                    transaction_type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (currency_id) REFERENCES currencies(id)
                )
            ''')

    def add_user(self, username, password):
        try:
            with self.connection:
                self.connection.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        user = self.connection.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        return user

    def add_currency(self, name, symbol):
        with self.connection:
            self.connection.execute('INSERT INTO currencies (name, symbol) VALUES (?, ?)', (name, symbol))

    def get_all_currencies(self):
        return self.connection.execute('SELECT * FROM currencies').fetchall()

    def add_transaction(self, user_id, currency_id, amount, price, transaction_type):
        with self.connection:
            self.connection.execute('INSERT INTO transactions (user_id, currency_id, amount, price, transaction_type) VALUES (?, ?, ?, ?, ?)',
                                    (user_id, currency_id, amount, price, transaction_type))

    def get_user_transactions(self, user_id):
        return self.connection.execute('SELECT t.id, c.name, c.symbol, t.amount, t.price, t.transaction_type, t.timestamp '
                                        'FROM transactions t '
                                        'JOIN currencies c ON t.currency_id = c.id '
                                        'WHERE t.user_id = ? ORDER BY t.timestamp DESC', (user_id,)).fetchall()
