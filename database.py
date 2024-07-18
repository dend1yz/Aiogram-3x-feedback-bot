import sqlite3

class Database:
    def __init__(self, db_file="database.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               user_id INTEGER UNIQUE,
                               username TEXT,
                               is_banned INTEGER DEFAULT 0
                               )""")
        self.conn.commit()

    def add_user(self, user_id, username):
        with self.conn:
            self.cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                                (user_id, username))

    def get_user_info(self, user_id_or_username):
        self.cursor.execute("SELECT * FROM users WHERE user_id=? OR username=?", 
                            (user_id_or_username, user_id_or_username))
        return self.cursor.fetchone()

    def ban_user(self, user_id):
        with self.conn:
            self.cursor.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,))

    def unban_user(self, user_id):
        with self.conn:
            self.cursor.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,))

    def is_user_banned(self, user_id):
        self.cursor.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result and result[0] == 1
