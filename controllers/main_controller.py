import sqlite3
import re
import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from utils.export_func import *
from utils.delete_func import delete_item


class Ui_Dialog(QMainWindow):
    def setupUi(self, MainWindow):
        """

        :type MainWindow: object
        """
        # Main window setup
        MainWindow.setObjectName("INVENTORY SYSTEM")
        icon_path = "assets/icons/inventory.png"
        MainWindow.setWindowIcon(QtGui.QIcon(icon_path))
        MainWindow.resize(986, 646)
        # MainWindow.setWindowState(Qt.WindowMaximized)

        #set size constraints
        MainWindow.setMinimumSize(QtCore.QSize(986, 646))
        MainWindow.setMaximumSize(QtCore.QSize(986, 646))

        # Set proper window flags
        MainWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowMinMaxButtonsHint |
            QtCore.Qt.WindowCloseButtonHint)

        # Set the window title explicitly
        MainWindow.setWindowTitle("INVENTORY SYSTEM")
        # print("Window title set:", MainWindow.windowTitle())

        # Tab widget for managing different views
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(0, 50, 981, 551))
        self.tabWidget.setObjectName("tabWidget")

        # Dashboard tab setup
        self.Dashboard = QtWidgets.QWidget()
        self.Dashboard.setObjectName("Dashboard")
        self.tabWidget.addTab(self.Dashboard, "")

        # Inventory tab setup
        # Add dashboard tab to tab widget
        self.Inventory = QtWidgets.QWidget()
        self.Inventory.setObjectName("Inventory")
        self.tabWidget.addTab(self.Inventory, "")

        # add_item tab setup
        # Add Item tab to tab widget
        self.add_item = QtWidgets.QWidget()
        self.add_item.setObjectName("Add item")
        self.tabWidget.addTab(self.add_item, "")

        #Delete_item tab setup
        #Delete item tab to tab widget
        self.delete_item = QtWidgets.QWidget()
        self.delete_item.setObjectName("delete_item")
        self.tabWidget.addTab(self.delete_item, "")


        # Table widget for displaying inventory data
        self.tableWidget = QtWidgets.QTableWidget(self.Inventory)
        self.tableWidget.setGeometry(QtCore.QRect(0, 40, 971, 481))
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        colnumHeaderName = ["ID", "Name", "Quantity", "Price"]
        self.tableWidget.setColumnCount(len(colnumHeaderName))
        self.tableWidget.setHorizontalHeaderLabels(colnumHeaderName)
        self.tableWidget.verticalHeader().setVisible(False)

        # Adjust column sizes
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # Resize "ID" column to fit contents
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)



        self.tableWidget.verticalHeader().setHighlightSections(True)

        # Enable row highlighting
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSortingEnabled(True)

        # Load data from database on startup
        self.load_data()


        # Refresh button to reload table data
        self.refereshbtn = QtWidgets.QPushButton(MainWindow)
        self.refereshbtn.setGeometry(QtCore.QRect(880, 610, 93, 28))
        self.refereshbtn.setObjectName("refereshbtn")
        self.refereshbtn.clicked.connect(self.load_data)  # Connect refresh button to data loading function

        # Enable row selection when a cell is clicked
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Set selection mode (optional, allows selecting only one row at a time)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


        # Horizontal layout for additional controls (top-right)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.Inventory)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(659, 0, 311, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #Button To Export Data
        self.pushExport_data = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushExport_data.setObjectName("pushExport_data")
        self.horizontalLayout.addWidget(self.pushExport_data)
        self.pushExport_data.clicked.connect(export_data)

        self.pushImport = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushImport.setObjectName("pushImport")
        self.horizontalLayout.addWidget(self.pushImport)

        # Horizontal layout for search functionality (top-left)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.Inventory)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 461, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Label for search input
        self.search = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.search.setFont(font)
        self.search.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.search.setObjectName("search")
        self.horizontalLayout_2.addWidget(self.search)

        # Line edit for search input
        self.search_lnput = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.search_lnput.textChanged.connect(self.update_filter)  # Connect search to filter function
        self.search_lnput.setText("")
        self.search_lnput.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.search_lnput.setObjectName("search_lnput")
        self.horizontalLayout_2.addWidget(self.search_lnput)






        # Title label for the window (Inventory Management)
        self.title = QtWidgets.QLabel(MainWindow)
        self.title.setGeometry(QtCore.QRect(0, 0, 991, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.title.setFont(font)
        self.title.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(45, 45, 75);")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")


        # Label to display the total count of items in the table
        self.totalcount = QtWidgets.QLabel(MainWindow)
        self.totalcount.setGeometry(QtCore.QRect(10, 620, 91, 16))
        self.totalcount.setObjectName("totalcount")

        # Label to display the actual count number
        self.totalcountN = QtWidgets.QLabel(MainWindow)
        self.totalcountN.setGeometry(QtCore.QRect(120, 620, 55, 16))
        self.totalcountN.setObjectName("totalcountN")

        # Retranslate the UI components to handle different languages if needed
        self.retranslateUi(MainWindow)

        # Set the default tab to be the second one (i.e., "ADD ITEM")
        self.tabWidget.setCurrentIndex(1)

        # Connect slots and signals for the UI
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "INVENTORY SYSTEM"))

            # Tab translations and setting the text for various labels and buttons
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.Dashboard), _translate("Dialog", "DASHBOARD"))


            self.tableWidget.setSortingEnabled(False)
            self.pushExport_data.setText(_translate("Dialog", "EXPORT"))
            self.pushImport.setText(_translate("Dialog", "IMPORT"))
            self.search.setText(_translate("Dialog", "Search"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.Inventory), _translate("Dialog", "INVENTORY DETAILS"))


            self.tabWidget.setTabText(self.tabWidget.indexOf(self.add_item), _translate("Dialog", "ADD ITEM"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.delete_item), _translate("Dialog", "DELETE ITEM"))


            self.title.setText(_translate("Dialog", "INVENTORY MANAGEMENT"))
            self.refereshbtn.setText(_translate("Dialog", "Refresh"))



            # Updating total count
            row_count = self.tableWidget.rowCount()
            self.totalcount.setText(_translate("Dialog", "TOTAL ROW :"))
            self.totalcountN.setText(_translate("Dialog", f"{row_count}"))

    def load_data(self):
        """Load data from SQLite database and populate the table."""
        try:
            connection = sqlite3.connect("database/inventory.db")
            cursor = connection.cursor()
            query = "SELECT * FROM products"
            cursor.execute(query)
            results = cursor.fetchall()

            # Reset the table and insert new data
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

                    # # Create an "Update" button for each row
                    # update_button = QtWidgets.QPushButton("Update")
                    # update_button.clicked.connect(partial(self.update_row, row_number))
                    # self.tableWidget.setCellWidget(row_number, 4, update_button)  # Add the button to the "Update" column

                    # # Create a "Delete" button for each row
                    # delete_button = QtWidgets.QPushButton("Delete")
                    # delete_button.clicked.connect(lambda: delete_item(self, row_number))
                    # self.tableWidget.setCellWidget(row_number, 5,
                    #                                delete_button)  # Add the button to the "Delete" columnt co
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    # def delete_row(self, row):
    #     """Delete the row from the table and database."""
    #     # Remove the row from the table
    #     self.tableWidget.removeRow(row)
    #
    #     # Get the ID of the item in the row to delete from the database
    #     item_id = self.tableWidget.item(row, 0).text()
    #
    #     # Delete the row from the database
    #     connection = sqlite3.connect("database/inventory.db")
    #     cursor = connection.cursor()
    #     query = "DELETE FROM products WHERE id = ?"
    #     cursor.execute(query, (item_id,))
    #     connection.commit()
    #
    #     # Refresh the table to reflect changes
    #     self.load_data()

    def update_row(self, row):
        """Update the row's data in the table and database."""
        # Get the updated values from the table for the row
        item_id = self.tableWidget.item(row, 0).text()
        item_name = self.tableWidget.item(row, 1).text()
        quantity = self.tableWidget.item(row, 2).text()
        price = self.tableWidget.item(row, 3).text()

        # Update the database with the new values
        connection = sqlite3.connect("database/inventory.db")
        cursor = connection.cursor()
        query = "UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?"
        cursor.execute(query, (item_name, quantity, price, item_id))
        connection.commit()

        # Show confirmation and refresh the table
        QtWidgets.QMessageBox.information(self, "Success", "Item Updated Successfully!")
        self.load_data()

    def save_update(self, product_id, name, category, price, stock, dialog):
        """Save the updated product data to the database."""
        connection = sqlite3.connect("database/inventory.db")
        cursor = connection.cursor()

        # Update the product in the database
        cursor.execute("""UPDATE products
                          SET name = ?, category = ?, price = ?, stock = ?
                          WHERE id = ?""", (name, category, price, stock, product_id))

        connection.commit()
        connection.close()

        # Close the update dialog and reload the data
        dialog.accept()
        self.load_data()





    #
    # def load_data(self):
    #         """Load data from SQLite database and populate the table."""
    #         connection = sqlite3.connect("database/inventory.db")
    #         cursor = connection.cursor()
    #
    #         query = "SELECT * FROM products"
    #         cursor.execute(query)
    #         results = cursor.fetchall()
    #
    #         # Resetting the table and inserting new data
    #         self.tableWidget.setRowCount(0)
    #         for row_number, row_data in enumerate(results):
    #             self.tableWidget.insertRow(row_number)
    #             for column_number, data in enumerate(row_data):
    #                 self.tableWidget.setItem(row_number,
    #                                          column_number,
    #                                          QtWidgets.QTableWidgetItem(str(data)))




    def update_filter(self, s):
        """Apply a filter to the table data based on the search string for ID and Name columns using regex."""
        # Create a regex pattern that matches the search string (case-insensitive)
        pattern = re.compile(re.escape(s), re.IGNORECASE)  # re.IGNORECASE for case-insensitive search

        row_count = self.tableWidget.rowCount()

        # Iterate through each row in the table
        for row in range(row_count):
            # Check both the ID (column 0) and Name (column 1)
            id_item = self.tableWidget.item(row, 0)  # ID is assumed to be in the first column
            name_item = self.tableWidget.item(row, 1)  # Name is assumed to be in the second column

            # Check if the search string matches either the ID or the Name using regex
            if id_item and name_item:
                # Search for the pattern in both ID and Name
                id_match = pattern.search(id_item.text()) is not None
                name_match = pattern.search(name_item.text()) is not None

                # Show row if either the ID or the Name matches
                if id_match or name_match:
                    self.tableWidget.setRowHidden(row, False)  # Show the row
                else:
                    self.tableWidget.setRowHidden(row, True)  # Hide the row
            else:
                self.tableWidget.setRowHidden(row, True)  # Hide row if either item is missing



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    MainWindow = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # app = QtWidgets.QApplication(sys.argv)
    #
    # # Create the main window
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_Dialog()
    # ui.setupUi(MainWindow)
    #
    # # Apply qtmodern styles and window
    # qtmodern.styles.dark(app)
    # modern_window = qtmodern.windows.ModernWindow(MainWindow)
    # modern_window.show()
    #
    # sys.exit(app.exec_())

