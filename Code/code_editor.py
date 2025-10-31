from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class CodeEdit(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.breakpoints = {}
        self.setup_editor()


    def setup_editor(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: #264f78;
            }
            QPlainTextEdit:focus {
                border: 1px solid #565656;
            }
        """)
