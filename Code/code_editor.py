from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from line_bar import*

class CodeEdit(QPlainTextEdit):
    def __init__(self, line_bar):
        super().__init__()
        self.line_bar = line_bar
        self.setup_editor()
        self.cursorPositionChanged.connect(self.on_cursor_moved)

    def setup_editor(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        block = cursor.block()
        line_text = block.text().strip()

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.line_bar.add_number()

        elif event.key() == Qt.Key_Backspace:
            if not line_text and self.line_bar.number > 1:
                self.line_bar.remove_number()

        super().keyPressEvent(event)

    def on_cursor_moved(self):
        line_number = self.textCursor().blockNumber() + 1
        self.line_bar.highlight_line(line_number)
