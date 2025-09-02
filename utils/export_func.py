import csv
import sqlite3
import pandas as pd
import os
import logging
import datetime
from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Set up logging: Create log folder if it doesn't exist and configure logging
log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
log_filename = os.path.join(log_folder, f"app_log_{current_date}.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logging.info("Export module started")

def export_data():
    """
    Exports data from the 'products' table in the SQLite database to an Excel file.
    The file is saved in the user's Downloads/Inventory Exports folder.
    """
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exports_folder = os.path.join(downloads_path, "Inventory Exports")

    try:
        logging.info("Creating exports folder if it doesn't exist.")
        # Create the exports folder if it doesn't exist
        os.makedirs(exports_folder, exist_ok=True)
        file_path = os.path.join(exports_folder, "exported_data.xlsx")
        logging.info(f"Export file will be saved to: {file_path}")

        # Connect to the SQLite database
        logging.info("Connecting to the database.")
        conn = sqlite3.connect("database/database.db")
        query = "SELECT * FROM products"
        df = pd.read_sql_query(query, conn)
        conn.close()
        logging.info("Data retrieved from the database successfully.")

        # Export the data to an Excel file
        df.to_excel(file_path, index=False)
        logging.info("Data exported to Excel file successfully.")

        # Show a confirmation message
        messageBoxConfirmation("Your data has been exported successfully!")
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)
        messageBoxConfirmation("Failed to export data due to a database error.", is_error=True)
    except Exception as e:
        logging.error("Data export failed: %s", e)
        messageBoxConfirmation("Failed to export data.", is_error=True)

def messageBoxConfirmation(message, is_error=False):
    """
    Displays a confirmation or error message box.

    :param message: The message to display.
    :param is_error: If True, displays an error message box. Otherwise, displays an information message box.
    """
    dlg = QMessageBox()
    dlg.setWindowTitle("Error" if is_error else "Confirmation")
    dlg.setIcon(QMessageBox.Critical if is_error else QMessageBox.Information)
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.exec_()
