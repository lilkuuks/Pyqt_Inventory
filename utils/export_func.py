import csv
import sqlite3
import pandas as pd
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog


def export_data():
    """
    Exports data from the 'products' table in the SQLite database to an Excel file.
    The file is saved in the user's Downloads/exports folder.
    """
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exports_folder = os.path.join(downloads_path, "Inventory Exports")

    try:
        # Create the exports folder if it doesn't exist
        os.makedirs(exports_folder, exist_ok=True)
        file_path = os.path.join(exports_folder, "exported_data.xlsx")

        # Connect to the SQLite database
        conn = sqlite3.connect("database/inventory.db")
        query = "SELECT * FROM products"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Export the data to an Excel file
        df.to_excel(file_path, index=False)

        # Show a confirmation message
        messageBoxConfirmation("Your data has been exported successfully!")
    except sqlite3.Error as e:
        print("Database error:", e)
        messageBoxConfirmation("Failed to export data due to a database error.", is_error=True)
    except Exception as e:
        print("Data export failed:", e)
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
