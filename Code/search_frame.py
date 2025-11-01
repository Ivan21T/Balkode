from PySide6.QtWidgets import*
from PySide6.QtCore import*
from PySide6.QtGui import*


class SearchFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(60)
        self.setStyleSheet("""
                    ActivityFrame {
                        background: #1e1e1e;
                        border: none;
                        border-right: 1px solid #2d2d2d;
                    }
                """)