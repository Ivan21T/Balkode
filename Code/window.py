import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from welcome_page import WelcomePage
from activity_bar import ActivityBar, observer
from status_bar import StatusBar
from code_editor import CodeEdit
from line_bar import LineBar
from search_frame import SearchFrame
from observer import Observer
from terminal import TerminalFrame

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Balkode")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignLeft)

        self.activity_bar = ActivityBar()
        self.line_bar=LineBar()
        self.editor_area = CodeEdit()
        self.search_frame = SearchFrame()
        self.terminal_frame = TerminalFrame()

        #Layout for code editor with terminal and line number
        self.code_area_widget = QWidget()
        self.layout_code_area = QHBoxLayout(self.code_area_widget)
        self.layout_code_area.addWidget(self.line_bar)
        self.layout_code_area.addWidget(self.editor_area)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.code_area_widget)
        self.splitter.addWidget(self.terminal_frame)
        self.splitter.setSizes([400, 200])

        self.editor_area.cursorPositionChanged.connect(self.update_cursor_position)
        observer.on_change.register(self.update_layout)

        self.main_layout.addWidget(self.activity_bar)
        self.main_layout.addWidget(self.splitter)

        self.main_layout.setStretch(0, 0)  # activity_bar won't stretch
        self.main_layout.setStretch(1, 1)  # splitter will take all remaining space
        self.central_widget.setLayout(self.main_layout)

        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

    def update_cursor_position(self):
        cursor = self.editor_area.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_bar.update_cursor_position(line, col)

    def update_layout(self,old_state,new_state):
        if new_state=="Explorer":
            self.main_layout.addWidget(self.line_bar)
            self.main_layout.addWidget(self.editor_area)
        elif new_state=="Search":
            if self.main_layout.count()>2:
                self.main_layout.removeWidget(self.line_bar)
                self.main_layout.removeWidget(self.editor_area)
                self.main_layout.addWidget(self.search_frame)
                self.main_layout.addWidget(self.line_bar)
                self.main_layout.addWidget(self.editor_area)
            else:
                self.main_layout.addWidget(self.search_frame)
        else:
            print("OK")
