#!/usr/bin/python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for handling SQLite DB connections"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering context"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection automatically, handle exceptions"""
        if self.conn:
            if exc_type is not None:
                # Rollback if there was an exception
                self.conn.rollback()
            else:
                # Commit if all went fine
                self.conn.commit()
            self.conn.close()
        # Returning False propagates exceptions if any
        return False


if __name__ == "__main__":
    # Use the context manager to fetch users
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
