import re
import sqlite3
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from utils.export_func import export_data
from utils.import_func import import_data
from gui_tabs.dashboard import DashboardTab


class Ui_Dialog(QMainWindow):
    def setupUi(self, MainWindow):
        """
        Setup the main window UI.
        :type MainWindow: QMainWindow
        """
        # Main window setup
        MainWindow.setObjectName("INVENTORY SYSTEM")
        icon_path = "assets/icons/inventory.png"
        MainWindow.setWindowIcon(QtGui.QIcon(icon_path))

        # Set initial window size (user can resize it)
        MainWindow.resize(986, 646)

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
        self.Dashboard = DashboardTab()
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

        # Layout for the Add Item tab
        self.add_item_layout = QtWidgets.QVBoxLayout(self.add_item)
        self.add_item_layout.setObjectName("add_item_layout")

        # Widgets for the Add Item tab

        # Item Name
        self.label_item_name = QtWidgets.QLabel(self.add_item)
        self.label_item_name.setObjectName("label_item_name")
        self.add_item_layout.addWidget(self.label_item_name)

        self.lineEdit_item_name = QtWidgets.QLineEdit(self.add_item)
        self.lineEdit_item_name.setObjectName("lineEdit_item_name")
        self.add_item_layout.addWidget(self.lineEdit_item_name)

        #Item Quantity
        self.label_item_quantity = QtWidgets.QLabel(self.add_item)
        self.label_item_quantity.setObjectName("label_item_quantity")
        self.add_item_layout.addWidget(self.label_item_quantity)

        self.lineEdit_item_quantity = QtWidgets.QLineEdit(self.add_item)
        self.lineEdit_item_quantity.setObjectName("lineEdit_item_quantity")
        self.add_item_layout.addWidget(self.lineEdit_item_quantity)

        # Item Price
        self.label_item_price = QtWidgets.QLabel(self.add_item)
        self.label_item_price.setObjectName("label_item_price")
        self.add_item_layout.addWidget(self.label_item_price)

        self.lineEdit_item_price = QtWidgets.QLineEdit(self.add_item)
        self.lineEdit_item_price.setObjectName("lineEdit_item_price")
        self.add_item_layout.addWidget(self.lineEdit_item_price)

        self.button_add_item = QtWidgets.QPushButton(self.add_item)
        self.button_add_item.setObjectName("button_add_item")
        self.add_item_layout.addWidget(self.button_add_item)

        # Spacer to push widgets to the top
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.add_item_layout.addItem(spacer)

        # Connect the Add Item button to a function
        self.button_add_item.clicked.connect(self.add_item_to_database)




        #Delete_item tab setup
        #Delete item tab to tab widget
        self.delete_item = QtWidgets.QWidget()
        self.delete_item.setObjectName("delete_item")
        self.tabWidget.addTab(self.delete_item, "")

        # Layout for the Delete Item tab
        self.delete_item_layout = QtWidgets.QVBoxLayout(self.delete_item)
        self.delete_item_layout.setObjectName("delete_item_layout")

        # Widgets for the Delete Item tab
        self.label_delete_item = QtWidgets.QLabel(self.delete_item)
        self.label_delete_item.setObjectName("label_delete_item")
        self.delete_item_layout.addWidget(self.label_delete_item)

        self.lineEdit_delete_item = QtWidgets.QLineEdit(self.delete_item)
        self.lineEdit_delete_item.setObjectName("lineEdit_delete_item")
        self.delete_item_layout.addWidget(self.lineEdit_delete_item)

        self.button_fetch_item = QtWidgets.QPushButton(self.delete_item)
        self.button_fetch_item.setObjectName("button_fetch_item")
        self.delete_item_layout.addWidget(self.button_fetch_item)

        # Spacer to push widgets to the top
        spacer_delete = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.delete_item_layout.addItem(spacer_delete)

        # Connect the fetch button to a function
        self.button_fetch_item.clicked.connect(self.fetch_item_for_deletion)


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
        self.pushImport.clicked.connect(import_data)

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

            # Set text for widgets in the Add Item tab
            self.label_item_name.setText(_translate("MainWindow", "Item Name:"))
            self.label_item_quantity.setText(_translate("MainWindow", "Item Quantity:"))
            self.label_item_price.setText(_translate("MainWindow", "Item Price:"))

            self.button_add_item.setText(_translate("MainWindow", "Add Item"))



            self.tabWidget.setTabText(self.tabWidget.indexOf(self.delete_item), _translate("Dialog", "DELETE ITEM"))

            # Set text for widgets in the Delete Item tab
            self.label_delete_item.setText(_translate("MainWindow", "Enter Item ID to Delete:"))
            self.button_fetch_item.setText(_translate("MainWindow", "Fetch Item"))



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

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))


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



    def fetch_item_for_deletion(self):
        """Fetch item data from the database and display it for confirmation."""
        item_id = self.lineEdit_delete_item.text().strip()

        if not item_id:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter an item ID.")
            return

        conn = None
        try:
            conn = sqlite3.connect("./database/inventory.db")  # Ensure correct DB path
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM products WHERE id = ?", (item_id,))
            item_data = cursor.fetchone()

            if not item_data:
                QtWidgets.QMessageBox.warning(self, "Not Found", "No item found with the given ID.")
                return

            confirmation_dialog = QMessageBox(self)
            confirmation_dialog.setIcon(QMessageBox.Question)
            confirmation_dialog.setWindowTitle("Confirm Deletion")
            confirmation_dialog.setText(f"Are you sure you want to delete this item?\n\n"
                                        f"ID: {item_data[0]}\n"
                                        f"Name: {item_data[1]}\n"
                                        f"Quantity: {item_data[2]}\n"
                                        f"Price: {item_data[3]}")
            confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation_dialog.setDefaultButton(QMessageBox.No)

            if confirmation_dialog.exec_() == QMessageBox.Yes:
                cursor.execute("DELETE FROM products WHERE id = ?", (item_id,))
                conn.commit()
                QMessageBox.information(self, "Success", "Item deleted successfully.")
                self.lineEdit_delete_item.clear()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()



    def add_item_to_database(self):
        """Add item data to the database."""
        # Get data from input fields
        item_name = self.lineEdit_item_name.text()
        item_quantity = self.lineEdit_item_quantity.text()
        item_price = self.lineEdit_item_price.text()

        # Validate input
        if not item_name or not item_quantity or not item_price:
            QtWidgets.QMessageBox.warning(None, "Input Error", "Please fill in all fields.")
            return

        try:
            # Convert quantity and price to appropriate types
            item_quantity = int(item_quantity)
            item_price = float(item_price)
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Input Error",
                                          "Quantity must be an integer and price must be a number.")
            return

        # Connect to the database
        conn = None
        try:
            conn = sqlite3.connect("database/inventory.db")
            cursor = conn.cursor()

            # Insert data into the products table
            cursor.execute(
                "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                (item_name, item_quantity, item_price)
            )
            conn.commit()

            # Show confirmation dialog
            QtWidgets.QMessageBox.information(None, "Success", "Item added successfully!")

            # Clear input fields
            self.lineEdit_item_name.clear()
            self.lineEdit_item_quantity.clear()
            self.lineEdit_item_price.clear()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

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

