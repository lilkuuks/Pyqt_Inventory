import csv
import sqlite3
import pandas as pd
import os
from PyQt5.QtWidgets import QMessageBox

"""This function exports the database into an cvs file"""


def export_data():
    #This code basically specifies the path where the exported file is saved
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    exports_folder = os.path.join(downloads_path, "exports")
    os.makedirs(exports_folder, exist_ok=True)
    file_path = os.path.join(exports_folder, "exported_data.xlsx")

    exported_bull = True
    try:
        conn = sqlite3.connect("database/inventory.db")
        query = "SELECT * FROM products"
        df = pd.read_sql_query(query, conn)
        df.to_excel(file_path, index=False)
        conn.close()
        messageBoxConfirmation()
    except Exception as e:
        print("Data export failed: ", e)






def messageBoxConfirmation():
    dlg = QMessageBox()
    dlg.resize(500, 500)
    dlg.setIcon(QMessageBox.Information)
    dlg.setWindowTitle("Confirmation")
    dlg.setText("Your Data is exported successfully")
    dlg.setStandardButtons(QMessageBox.Ok)
    button = dlg.exec_()
    if button == QMessageBox.Ok:
        print("Exported!!")



def import_data(self):
    print("Imported!!")