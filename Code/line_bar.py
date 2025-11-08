from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

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
        self.number = 1
        self.add_number()

    def setup_line_number_bar(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 5, 0, 5)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def add_number(self):
        number_label = QLabel(str(self.number))
        number_label.setAlignment(Qt.AlignCenter)
        number_label.setStyleSheet("""
            color: white;
            font-family: Consolas;
            font-size: 12px;
        """)
        number_label.setObjectName(str(self.number))
        self.layout.addWidget(number_label)
        self.number += 1

    def remove_number(self):
        if self.layout.count() > 1:
            item = self.layout.takeAt(self.layout.count() - 1)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            self.number -= 1

    def highlight_line(self, line_number):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget:
                if int(widget.objectName()) == line_number:
                    widget.setStyleSheet("color: cyan; font-family: Consolas; font-size: 12px;")
                else:
                    widget.setStyleSheet("color: white; font-family: Consolas; font-size: 12px;")