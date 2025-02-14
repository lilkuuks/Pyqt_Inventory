import csv

from PyQt5.QtWidgets import QMessageBox

"""This function exports the database into an cvs file"""


def export_data():

    exported_bull = True
    messageBoxConfirmation()




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