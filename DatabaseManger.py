import os
import sys
import sqlite3
import logging


class DatabaseManager:
    def __init__(self):
        self.db_path = self.get_database_path()

    def get_database_path(self):
        """
        Get the correct database path for both development and packaged app.
        If running as a PyInstaller bundle, store DB in a writable directory.
        """
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            base_dir = os.path.dirname(sys.executable)
        else:
            # Running in normal Python environment
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # Use a writable path for the database
        db_dir = os.path.join(base_dir, "database")
        os.makedirs(db_dir, exist_ok=True)

        return os.path.join(db_dir, "database.db")

    def get_connection(self):
        """Establish database connection and initialize if needed"""
        try:
            connection = sqlite3.connect(self.db_path)
            self.initialize_database(connection)
            return connection
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            raise

    def initialize_database(self, connection):
        """Create tables if they don't exist"""
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products
            (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                category     TEXT,
                quantity     INTEGER,
                price        REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        connection.commit()

    def load_products(self):
        """Load all products from database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products")
            results = cursor.fetchall()
            connection.close()
            return results
        except Exception as e:
            logging.error(f"Error loading products: {e}")
            return []
