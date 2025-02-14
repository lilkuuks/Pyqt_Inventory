import sqlite3
from PyQt5.QtWidgets import QMessageBox

def delete_item(self, row):
    """Handle the deletion of the row."""
    # Get the item ID from the first column (assuming it's an integer ID)
    item_id = self.tableWidget.item(row, 0).text()

    # Confirm the deletion with the user
    reply = QMessageBox.question(self, 'Delete Item',
                                 f"Are you sure you want to delete item with ID {item_id}?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        # Delete the item from the database
        connection = sqlite3.connect("database/inventory.db")
        cursor = connection.cursor()
        query = "DELETE FROM products WHERE id = ?"
        cursor.execute(query, (item_id,))
        connection.commit()

        # Now delete the row from the table
        self.tableWidget.removeRow(row)

        # Refresh the table to reflect changes
        self.load_data()
        QMessageBox.information(self, "Success", "Item Deleted Successfully!")
    else:
        QMessageBox.information(self, "Cancelled", "Item deletion cancelled.")
