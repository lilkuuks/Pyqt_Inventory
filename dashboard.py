# dashboard.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DashboardTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the dashboard
        self.layout = QVBoxLayout(self)

        # Add a title
        self.title = QLabel("Dashboard")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Add key metrics
        self.add_key_metrics()

        # Add a chart
        self.add_chart()

        # Add recent activity table
        self.add_recent_activity()

        # Add quick action buttons
        self.add_quick_actions()

    def add_key_metrics(self):
        """Add key metrics like total items and total value."""
        # Fetch data from the database
        total_items, total_value = self.fetch_key_metrics()

        # Create labels to display the metrics
        self.label_total_items = QLabel(f"Total Items: {total_items}")
        self.label_total_value = QLabel(f"Total Inventory Value: ${total_value:.2f}")

        # Add to layout
        self.layout.addWidget(self.label_total_items)
        self.layout.addWidget(self.label_total_value)

    def fetch_key_metrics(self):
        """Fetch total items and total value from the database."""
        conn = sqlite3.connect("database/inventory.db")
        cursor = conn.cursor()

        # Fetch total items
        cursor.execute("SELECT COUNT(*) FROM products")
        total_items = cursor.fetchone()[0]

        # Fetch total value
        cursor.execute("SELECT SUM(quantity * price) FROM products")
        total_value = cursor.fetchone()[0] or 0  # Handle case where table is empty

        conn.close()
        return total_items, total_value

    def add_chart(self):
        """Add a bar chart to visualize inventory data."""
        # Fetch data for the chart
        items, quantities = self.fetch_chart_data()

        # Create a matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Create a bar chart
        ax = self.figure.add_subplot(111)
        ax.bar(items, quantities)
        ax.set_xlabel("Items")
        ax.set_ylabel("Quantity")
        ax.set_title("Inventory Quantities")

        # Add the chart to the layout
        self.layout.addWidget(self.canvas)

    def fetch_chart_data(self):
        """Fetch item names and quantities for the chart."""
        conn = sqlite3.connect("database/inventory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name, quantity FROM products")
        data = cursor.fetchall()

        conn.close()

        # Separate item names and quantities
        items = [row[0] for row in data]
        quantities = [row[1] for row in data]

        return items, quantities

    def add_recent_activity(self):
        """Add a table to show recent activity."""
        self.recent_activity_table = QTableWidget()
        self.recent_activity_table.setColumnCount(4)
        self.recent_activity_table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Price"])

        # Fetch recent activity data
        self.load_recent_activity()

        # Add the table to the layout
        self.layout.addWidget(self.recent_activity_table)

    def load_recent_activity(self):
        """Load recent activity data into the table."""
        conn = sqlite3.connect("database/inventory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products ORDER BY id DESC LIMIT 10")  # Fetch last 10 items
        rows = cursor.fetchall()

        self.recent_activity_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.recent_activity_table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        conn.close()

    def add_quick_actions(self):
        """Add buttons for quick actions."""
        self.button_add_item = QPushButton("Add Item")
        self.button_delete_item = QPushButton("Delete Item")

        # Add buttons to layout
        self.layout.addWidget(self.button_add_item)
        self.layout.addWidget(self.button_delete_item)