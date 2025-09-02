import csv
import sqlite3
import os
import logging
import datetime
from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Set up logging: Create a log folder and a daily log file
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
logging.info("Import module started")

def import_data():
    """
    Imports data from a CSV file into the 'products' table in the SQLite database.
    """
    logging.info("Starting data import process.")
    try:
        # Open a file dialog to select the CSV file
        file_path, _ = QFileDialog.getOpenFileName(None, "Select CSV File", "", "CSV Files (*.csv)")
        logging.debug(f"File selected: {file_path}")

        if file_path:
            # Connect to the SQLite database
            logging.info("Connecting to the database.")
            conn = sqlite3.connect("database/database.db")
            cursor = conn.cursor()

            # Read the CSV file
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row
                logging.debug(f"CSV Header: {header}")

                row_count = 0
                # Insert data into the 'products' table
                for row in reader:
                    logging.debug(f"Inserting row: {row}")
                    cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?)", row)
                    row_count += 1

            conn.commit()
            conn.close()
            logging.info(f"Data import successful. {row_count} rows imported.")
            # Show a confirmation message
            messageBoxConfirmation("Data imported successfully!")
        else:
            logging.info("No file selected. Import canceled.")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        messageBoxConfirmation("Failed to import data due to a database error.", is_error=True)
    except Exception as e:
        logging.error(f"Data import failed: {e}")
        messageBoxConfirmation("Failed to import data.", is_error=True)

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
