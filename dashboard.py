# dashboard.py
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QFrame
from PyQt5.QtChart import QChart, QChartView, QPieSeries


def setup_dashboard(parent):
    """Set up a modern and visually appealing dashboard tab."""

    # Create Dashboard tab
    parent.Dashboard = QtWidgets.QWidget()
    parent.Dashboard.setObjectName("Dashboard")

    main_layout = QVBoxLayout(parent.Dashboard)

    # ====== Summary Panel ======
    summary_frame = QFrame()
    summary_frame.setFrameShape(QFrame.StyledPanel)
    summary_layout = QHBoxLayout(summary_frame)

    summary_data = [
        ("Total Products", "120"),
        ("Low Stock Items", "5"),
        ("Total Sales", "$15,240"),
        ("Pending Orders", "8")
    ]

    for title, value in summary_data:
        box = QFrame()
        box.setFrameShape(QFrame.StyledPanel)
        box.setStyleSheet("background: #f4f4f4; border-radius: 10px; padding: 10px;")

        vbox = QVBoxLayout(box)
        label_title = QLabel(title)
        label_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        label_value = QLabel(value)
        label_value.setStyleSheet("font-size: 18px; color: #007bff;")

        vbox.addWidget(label_title)
        vbox.addWidget(label_value)
        summary_layout.addWidget(box)

    main_layout.addWidget(summary_frame)

    # ====== Recent Transactions Table ======
    table_frame = QFrame()
    table_frame.setFrameShape(QFrame.StyledPanel)
    table_layout = QVBoxLayout(table_frame)

    label_table = QLabel("Recent Transactions")
    label_table.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
    table_layout.addWidget(label_table)

    parent.transaction_table = QTableWidget()
    parent.transaction_table.setColumnCount(3)
    parent.transaction_table.setHorizontalHeaderLabels(["Date", "Item", "Amount"])
    parent.transaction_table.setRowCount(3)

    transactions = [
        ("2025-02-14", "Laptop", "$1200"),
        ("2025-02-13", "Keyboard", "$150"),
        ("2025-02-12", "Monitor", "$300"),
    ]

    for row, data in enumerate(transactions):
        for col, value in enumerate(data):
            parent.transaction_table.setItem(row, col, QTableWidgetItem(value))

    parent.transaction_table.setStyleSheet("background: white; border-radius: 5px;")
    parent.transaction_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    parent.transaction_table.horizontalHeader().setStretchLastSection(True)

    table_layout.addWidget(parent.transaction_table)
    main_layout.addWidget(table_frame)

    # ====== Sales Chart ======
    chart_frame = QFrame()
    chart_frame.setFrameShape(QFrame.StyledPanel)
    chart_layout = QVBoxLayout(chart_frame)

    label_chart = QLabel("Sales Distribution")
    label_chart.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
    chart_layout.addWidget(label_chart)

    series = QPieSeries()
    series.append("Electronics", 50)
    series.append("Accessories", 30)
    series.append("Software", 20)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Sales by Category")
    chart.legend().setVisible(True)

    chart_view = QChartView(chart)
    chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

    chart_layout.addWidget(chart_view)
    main_layout.addWidget(chart_frame)

    parent.tabWidget.addTab(parent.Dashboard, "Dashboard")
