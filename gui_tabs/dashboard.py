import os
import logging
import datetime
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QFrame, QSizePolicy)

# Set up logging: Create log folder if it doesn't exist and configure logging
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
logging.info("Application started")
    
class DashboardTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        logging.info("Initializing DashboardTab UI")
        self.init_ui()
        self.load_data()

    def init_ui(self):
        logging.debug("Setting up UI layouts and widgets")
        # Main layout for the Dashboard tab
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Header: Title and Refresh Button
        self.header = QHBoxLayout()
        self.title = QLabel("Inventory Dashboard")
        self.title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold;
            color: #2c3e50;
        """)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.setIcon(QtGui.QIcon("assets/icons/refresh.png"))
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.refresh_btn.clicked.connect(self.load_data)

        self.header.addWidget(self.title)
        self.header.addStretch()
        self.header.addWidget(self.refresh_btn)
        self.main_layout.addLayout(self.header)

        # Metrics cards layout
        self.metrics_layout = QHBoxLayout()
        self.metrics_layout.setSpacing(15)

        # Create metric cards
        self.total_items_card = self.create_metric_card("Total Items", "0", "#3498db", "assets/icons/box.png")
        self.total_value_card = self.create_metric_card("Total Value", "$0", "#2ecc71", "assets/icons/dollar.png")
        self.low_stock_card = self.create_metric_card("Low Stock Items", "0", "#e74c3c", "assets/icons/warning.png")

        # Set expanding horizontally for each card
        for card in [self.total_items_card, self.total_value_card, self.low_stock_card]:
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.metrics_layout.addWidget(card)

        self.main_layout.addLayout(self.metrics_layout)

        # Content Layout: Charts and Recent Activity
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(20)

        # Chart Container
        self.chart_container = QFrame()
        self.chart_container.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            padding: 10px;
        """)
        self.chart_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart_layout = QVBoxLayout(self.chart_container)
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart_layout.addWidget(self.canvas)
        self.content_layout.addWidget(self.chart_container, 3)  # stretch factor 3

        # Recent Activity Container
        self.recent_activity_container = QFrame()
        self.recent_activity_container.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            padding: 10px;
        """)
        self.recent_activity_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.recent_layout = QVBoxLayout(self.recent_activity_container)

        self.recent_title = QLabel("Recent Activity")
        self.recent_title.setStyleSheet("font-size: 16px; font-weight: 500;")
        self.recent_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.recent_layout.addWidget(self.recent_title)

        self.recent_activity_table = QTableWidget()
        self.recent_activity_table.setColumnCount(4)
        self.recent_activity_table.setHorizontalHeaderLabels(["ID", "Name", "Qty", "Price"])
        self.recent_activity_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.recent_activity_table.verticalHeader().setVisible(False)
        self.recent_activity_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.recent_activity_table.setStyleSheet("""
            QTableWidget {
                border: none;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 6px;
            }
        """)
        self.recent_activity_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.recent_layout.addWidget(self.recent_activity_table)
        self.content_layout.addWidget(self.recent_activity_container, 2)  # stretch factor 2

        self.main_layout.addLayout(self.content_layout)

        # Quick Actions Layout (smaller buttons to leave more space for the chart)
        self.quick_actions = QHBoxLayout()
        self.quick_actions.setSpacing(10)

        buttons = [
            ("Add Item", "#2ecc71", "assets/icons/add.png"),
            ("Delete Item", "#e74c3c", "assets/icons/delete.png"),
            ("Export Data", "#3498db", "assets/icons/export.png")
        ]

        for text, color, icon in buttons:
            btn = QPushButton(text)
            btn.setIcon(QtGui.QIcon(icon))
            btn.setStyleSheet(f"""
                QPushButton {{
                    padding: 5px 10px;
                    border-radius: 4px;
                    background-color: {color};
                    color: white;
                    font-weight: 500;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setFixedHeight(30)
            btn.setFixedWidth(100)
            self.quick_actions.addWidget(btn)

        self.main_layout.addLayout(self.quick_actions)
        logging.info("UI initialization complete.")

    def create_metric_card(self, title, value, color, icon_path):
        card = QFrame()
        card.setStyleSheet(f"""
            background-color: {color};
            border-radius: 8px;
            padding: 15px;
            color: white;
        """)
        layout = QHBoxLayout(card)
        icon_label = QLabel()
        icon_label.setPixmap(QtGui.QIcon(icon_path).pixmap(40, 40))
        icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(icon_label)
        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignCenter)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        layout.addLayout(text_layout)
        logging.debug(f"Metric card '{title}' created with initial value '{value}'.")
        return card

    def darken_color(self, hex_color, factor=0.8):
        """Darken a hex color by a factor (0-1)"""
        color = QtGui.QColor(hex_color)
        darkened = color.darker(int(100 + (100 * (1 - factor)))).name()
        # logging.debug(f"Color {hex_color} darkened to {darkened}.")
        return darkened

    def load_data(self):
        logging.info("Loading data from the database.")
        try:
            conn = sqlite3.connect("database/inventory.db")
            cursor = conn.cursor()

            # Total Items
            cursor.execute("SELECT COUNT(*) FROM products")
            total_items = cursor.fetchone()[0]
            total_items_label = self.total_items_card.findChildren(QLabel)[1]
            total_items_label.setText(str(total_items))
            logging.debug(f"Total items: {total_items}")

            # Total Value
            cursor.execute("SELECT SUM(quantity * price) FROM products")
            total_value = cursor.fetchone()[0] or 0
            total_value_label = self.total_value_card.findChildren(QLabel)[1]
            total_value_label.setText(f"${total_value:,.2f}")
            logging.debug(f"Total value: ${total_value:,.2f}")

            # Low Stock
            cursor.execute("SELECT COUNT(*) FROM products WHERE quantity < 10")
            low_stock = cursor.fetchone()[0]
            low_stock_label = self.low_stock_card.findChildren(QLabel)[1]
            low_stock_label.setText(str(low_stock))
            logging.debug(f"Low stock items: {low_stock}")

            self.update_chart(cursor)
            self.update_recent_activity(cursor)
            conn.close()
            logging.info("Data loaded and UI updated successfully.")
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def update_chart(self, cursor):
        logging.info("Updating chart.")
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        cursor.execute("SELECT name, quantity FROM products ORDER BY quantity DESC LIMIT 5")
        data = cursor.fetchall()
        if data:
            items = [row[0] for row in data]
            quantities = [row[1] for row in data]
            bars = ax.bar(items, quantities, color='#3498db')
            ax.set_ylabel('Quantity')
            ax.set_title('Top 5 Stock Items')
            try:
                ax.bar_label(bars, padding=3)
            except Exception:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{height}', ha='center', va='bottom', fontsize=9)
            logging.debug(f"Chart updated with data: {data}")
        else:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=12, color='gray')
            logging.debug("No data available for chart.")
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha("right")
        self.figure.tight_layout()
        self.canvas.draw()
        logging.info("Chart drawing complete.")

    def update_recent_activity(self, cursor):
        logging.info("Updating recent activity table.")
        self.recent_activity_table.setRowCount(0)
        cursor.execute("SELECT * FROM products ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        if not rows:
            logging.debug("No recent activity found.")
            return
        self.recent_activity_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                if col_idx == 3:  # Format Price column
                    try:
                        item.setText(f"${float(col_data):.2f}")
                    except (ValueError, TypeError):
                        pass
                self.recent_activity_table.setItem(row_idx, col_idx, item)
        logging.info("Recent activity table updated.")

logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
