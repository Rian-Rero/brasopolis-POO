import sqlite3

class Database:
    def __init__(self, db_name="game_records.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def insert_record(self, player_name, score):
        with self.connection:
            self.connection.execute("""
                INSERT INTO records (player_name, score)
                VALUES (?, ?)
            """, (player_name, score))

    def get_all_records(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM records").fetchall()

    def close(self):
        self.connection.close()