import csv
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QFileDialog


def import_data():
    """
    Imports data from a CSV file into the 'products' table in the SQLite database.
    """
    try:
        # Open a file dialog to select the CSV file
        file_path, _ = QFileDialog.getOpenFileName(None, "Select CSV File", "", "CSV Files (*.csv)")

        if file_path:
            # Connect to the SQLite database
            conn = sqlite3.connect("database/inventory.db")
            cursor = conn.cursor()

            # Read the CSV file
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row

                # Insert data into the 'products' table
                for row in reader:
                    cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?)", row)

            conn.commit()
            conn.close()

            # Show a confirmation message
            messageBoxConfirmation("Data imported successfully!")
    except sqlite3.Error as e:
        print("Database error:", e)
        messageBoxConfirmation("Failed to import data due to a database error.", is_error=True)
    except Exception as e:
        print("Data import failed:", e)
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