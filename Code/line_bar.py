from PySide6.QtWidgets import*
from PySide6.QtCore import*
from PySide6.QtGui import*


class LineBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(30)
        self.setStyleSheet("""
            LineBar {
                background: #1e1e1e;
                border: none;
                border-right: 1px solid #2d2d2d;
            }
        """)
        self.setup_line_number_bar()

    def setup_line_number_bar(self):
        layout = QVBoxLayout()
        self.setLayout(layout)