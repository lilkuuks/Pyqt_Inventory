import sys
import re
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from openpyxl.styles.builtins import total

from utils.export_func import export_data
from utils.import_func import import_data
from gui_tabs.dashboard import DashboardTab
from DatabaseManger import DatabaseManager


class Ui_Dialog(QMainWindow):
    def setupUi(self, MainWindow):
        """
        Setup the main window UI.
        :type MainWindow: QMainWindow
        """
        # Main window setup
        MainWindow.setObjectName("INVENTORY SYSTEM")
        icon_path = "assets/inventory.png"
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

        # Delete_item tab setup
        # Delete item tab to tab widget
        self.update_item = QtWidgets.QWidget()
        self.delete_item.setObjectName("update_item")
        self.tabWidget.addTab(self.update_item, "")

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

            self.tabWidget.setTabText(self.tabWidget.indexOf(self.update_item), _translate("Dialog", "UPDATE ITEM"))

            # Set text for widgets in the Delete Item tab
            self.label_delete_item.setText(_translate("MainWindow", "Enter Item ID to Delete:"))
            self.button_fetch_item.setText(_translate("MainWindow", "Fetch Item"))



            self.title.setText(_translate("Dialog", "INVENTORY MANAGEMENT"))
            self.refereshbtn.setText(_translate("Dialog", "Refresh"))

            # Update total count
            row_count = self.tableWidget.rowCount()
            self.totalcount.setText(_translate("Dialog", f"Total Rows: {total_rows}"))
            # self.totalcountN.setText(_translate("Dialog", str(row_count)))

    def load_data(self):
        """Load data from SQLite database and populate the table."""
        try:
            db_manager = DatabaseManager()
            results = db_manager.load_products()

            # Log the number of rows loaded
            logging.info(f"Loaded {len(results)} rows from the database.")
            global total_rows
            total_rows = len(results)

            # Reset the table and insert new data
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(results):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number,
                                             QtWidgets.QTableWidgetItem(str(data)))
            logging.debug("Table widget updated with new data.")

        except Exception as e:
            logging.error(f"Error loading data: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def update_row(self, row):
        """Update the row's data in the table and database."""
        try:
            logging.info("Starting update for row %s.", row)

            # Get the updated values from the table for the row
            item_id = self.tableWidget.item(row, 0).text()
            item_name = self.tableWidget.item(row, 1).text()
            quantity = self.tableWidget.item(row, 2).text()
            price = self.tableWidget.item(row, 3).text()
            logging.debug("Row %s data: ID=%s, Name=%s, Quantity=%s, Price=%s", row, item_id, item_name, quantity,
                          price)

            # Update the database with the new values using DatabaseManager
            db_manager = DatabaseManager()
            connection = db_manager.get_connection()
            cursor = connection.cursor()
            query = "UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?"
            cursor.execute(query, (item_name, quantity, price, item_id))
            connection.commit()
            connection.close()
            logging.info("Row %s updated successfully in the database.", row)

            # Show confirmation and refresh the table
            QtWidgets.QMessageBox.information(self, "Success", "Item Updated Successfully!")
            self.load_data()

        except Exception as e:
            logging.error("Error updating row %s: %s", row, e)
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def save_update(self, product_id, name, category, price, stock, dialog):
        """Save the updated product data to the database."""
        try:
            logging.info("Saving update for product ID: %s", product_id)

            # Use DatabaseManager for connection
            db_manager = DatabaseManager()
            connection = db_manager.get_connection()
            cursor = connection.cursor()

            # Update the product in the database
            cursor.execute(
                """UPDATE products
                   SET name     = ?,
                       category = ?,
                       price    = ?,
                       quantity = ?
                   WHERE id = ?""",
                (name, category, price, stock, product_id)
            )
            connection.commit()
            connection.close()
            logging.info("Product ID %s updated successfully.", product_id)

            # Close the update dialog and reload the data
            dialog.accept()
            self.load_data()
        except Exception as e:
            logging.error("Error saving update for product ID %s: %s", product_id, e)
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def update_filter(self, s):
        """Apply a filter to the table data based on the search string for ID and Name columns using regex."""
        try:
            # Create a regex pattern that matches the search string (case-insensitive)
            pattern = re.compile(re.escape(s), re.IGNORECASE)
            row_count = self.tableWidget.rowCount()
            logging.info("Applying filter '%s' to %d rows.", s, row_count)

            # Iterate through each row in the table
            for row in range(row_count):
                # Check both the ID (column 0) and Name (column 1)
                id_item = self.tableWidget.item(row, 0)
                name_item = self.tableWidget.item(row, 1)

                # Check if the search string matches either the ID or the Name using regex
                if id_item and name_item:
                    id_match = pattern.search(id_item.text()) is not None
                    name_match = pattern.search(name_item.text()) is not None

                    # Show row if either the ID or the Name matches; otherwise hide the row
                    if id_match or name_match:
                        self.tableWidget.setRowHidden(row, False)
                    else:
                        self.tableWidget.setRowHidden(row, True)
                else:
                    self.tableWidget.setRowHidden(row, True)
            logging.debug("Filter applied successfully.")
        except Exception as e:
            logging.error("Error applying filter: %s", e)

    def fetch_item_for_deletion(self):
        """Fetch item data from the database and display it for confirmation."""
        item_id = self.lineEdit_delete_item.text().strip()
        if not item_id:
            logging.warning("No item ID provided for deletion.")
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter an item ID.")
            return

        try:
            logging.info("Fetching item with ID: %s", item_id)

            # Use DatabaseManager for connection
            db_manager = DatabaseManager()
            connection = db_manager.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products WHERE id = ?", (item_id,))
            item_data = cursor.fetchone()

            if not item_data:
                logging.warning("No item found with ID: %s", item_id)
                QtWidgets.QMessageBox.warning(self, "Not Found", "No item found with the given ID.")
                return

            logging.info("Item found: %s", item_data)
            confirmation_dialog = QtWidgets.QMessageBox(self)
            confirmation_dialog.setIcon(QtWidgets.QMessageBox.Question)
            confirmation_dialog.setWindowTitle("Confirm Deletion")
            confirmation_dialog.setText(f"Are you sure you want to delete this item?\n\n"
                                        f"ID: {item_data[0]}\n"
                                        f"Name: {item_data[1]}\n"
                                        f"Quantity: {item_data[3]}\n"  # Fixed index based on your table structure
                                        f"Price: {item_data[4]}")  # Fixed index based on your table structure
            confirmation_dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirmation_dialog.setDefaultButton(QtWidgets.QMessageBox.No)

            if confirmation_dialog.exec_() == QtWidgets.QMessageBox.Yes:
                cursor.execute("DELETE FROM products WHERE id = ?", (item_id,))
                connection.commit()
                logging.info("Item with ID %s deleted successfully.", item_id)
                QtWidgets.QMessageBox.information(self, "Success", "Item deleted successfully.")
                self.lineEdit_delete_item.clear()
            else:
                logging.info("Deletion cancelled by user for item ID %s.", item_id)

            connection.close()
        except Exception as e:
            logging.error("Database error during deletion: %s", e)
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

    def add_item_to_database(self):
        """Add item data to the database."""
        logging.info("Adding a new item to the database.")
        # Get data from input fields and remove extra whitespace
        item_name = self.lineEdit_item_name.text().strip()
        item_quantity = self.lineEdit_item_quantity.text().strip()
        item_price = self.lineEdit_item_price.text().strip()

        # Validate input
        if not item_name or not item_quantity or not item_price:
            logging.warning("Input error: One or more fields are empty.")
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        try:
            # Convert quantity and price to appropriate types
            item_quantity = int(item_quantity)
            item_price = float(item_price)
        except ValueError as e:
            logging.error("Conversion error: %s", e)
            QtWidgets.QMessageBox.warning(self, "Input Error",
                                          "Quantity must be an integer and price must be a number.")
            return

        try:
            logging.info("Connecting to the database for adding a new item.")

            # Use DatabaseManager for connection
            db_manager = DatabaseManager()
            connection = db_manager.get_connection()
            cursor = connection.cursor()

            # Retrieve all existing item names from the database
            cursor.execute("SELECT name FROM products")
            existing_names = [row[0] for row in cursor.fetchall()]
            logging.debug("Existing names in database: %s", existing_names)

            # Use regex to check for an exact match (case-sensitive)
            duplicate_found = any(
                re.fullmatch(re.escape(existing), item_name) for existing in existing_names
            )
            if duplicate_found:
                logging.warning("Duplicate item detected: %s", item_name)
                QtWidgets.QMessageBox.warning(self, "Duplicate Item",
                                              "An item with this name already exists in the database.")
                return

            # Insert data into the products table if no duplicate found
            cursor.execute(
                "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                (item_name, item_quantity, item_price)
            )
            connection.commit()
            logging.info("Item '%s' added successfully.", item_name)

            # Show confirmation dialog and clear input fields
            QtWidgets.QMessageBox.information(self, "Success", "Item added successfully!")
            self.lineEdit_item_name.clear()
            self.lineEdit_item_quantity.clear()
            self.lineEdit_item_price.clear()

            connection.close()
        except Exception as e:
            logging.error("Database error when adding item: %s", e)
            QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")


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

