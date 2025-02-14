import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class TableWidgetExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QTableWidget Row Highlight Example')

        # Create a QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)

        # Populate the table with some data
        for i in range(5):
            for j in range(3):
                self.tableWidget.setItem(i, j, QTableWidgetItem(f'Item {i},{j}'))

        # Connect the cellClicked signal to a custom slot
        self.tableWidget.cellClicked.connect(self.highlightRow)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def highlightRow(self, row, column):
        # Select the entire row
        self.tableWidget.selectRow(row)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableWidgetExample()
    ex.show()
    sys.exit(app.exec_())