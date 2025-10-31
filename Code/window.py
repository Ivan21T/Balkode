import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from activity_bar import ActivityBar
from status_bar import StatusBar
from code_editor import CodeEdit
from line_bar import LineBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Balkode")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.activity_bar = ActivityBar()
        self.line_bar=LineBar()
        self.editor_area = CodeEdit()
        self.editor_area.cursorPositionChanged.connect(self.update_cursor_position)

        main_layout.addWidget(self.activity_bar)
        main_layout.addWidget(self.line_bar)
        main_layout.addWidget(self.editor_area)

        central_widget.setLayout(main_layout)

        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

    def update_cursor_position(self):
        cursor = self.editor_area.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_bar.update_cursor_position(line, col)