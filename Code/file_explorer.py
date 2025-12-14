import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class FileExplorer(QFrame):
    def __init__(self, parent=None, start_path=None):
        super().__init__(parent)
        self.code_area = None
        self.setup_ui(start_path)

    def setup_ui(self, start_path):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setFixedHeight(30)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 10, 0)

        title_label = QLabel("EXPLORER")
        title_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-weight: bold;
                font-size: 11px;
            }
        """)

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.new_file_btn = self.create_header_button("+")
        self.refresh_btn = self.create_header_button("↻")

        header_layout.addWidget(self.new_file_btn)
        header_layout.addWidget(self.refresh_btn)

        layout.addWidget(header_frame)

        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        self.tree_view.setModel(self.model)

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: none;
            }
        """)

        self.tree_view.setStyleSheet("""
            QTreeView {
                background-color: #252526;
                color: #cccccc;
                border: none;
                outline: none;
                font-size: 13px;
            }
            QTreeView::item {
                background-color: #252526;
                padding: 2px;
                height: 22px;
                border: none;
            }
            QTreeView::item:hover {
                background-color: #2a2d2e;
            }
            QTreeView::item:selected {
                background-color: #094771;
                color: white;
            }
        """)

        if start_path is None:
            start_path = QDir.homePath()

        self.tree_view.setRootIndex(self.model.index(start_path))
        self.tree_view.doubleClicked.connect(self.on_double_clicked)

        layout.addWidget(self.tree_view)

        self.refresh_btn.clicked.connect(self.refresh_view)
        self.new_file_btn.clicked.connect(self.create_new_file)

    def create_header_button(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(20, 20)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #cccccc;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2a2d2e;
            }
            QPushButton:pressed {
                background-color: #094771;
            }
        """)
        return btn

    def on_double_clicked(self, index):
        path = self.model.filePath(index)
        if not self.model.isDir(index) and self.code_area:
            self.load_file(path)

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.code_area.setPlainText(content)
            self.current_file_path = path
        except Exception as e:
            self.code_area.setPlainText(f"Error reading file: {str(e)}")

    def set_code_area(self, code_area):
        self.code_area = code_area

    def refresh_view(self):
        current_index = self.tree_view.currentIndex()
        self.tree_view.setRootIndex(self.model.index(self.model.rootPath()))

    def create_new_file(self):
        current_index = self.tree_view.currentIndex()
        if current_index.isValid():
            current_path = self.model.filePath(current_index)
            if self.model.isDir(current_index):
                directory = current_path
            else:
                directory = os.path.dirname(current_path)

            filename, ok = QInputDialog.getText(self, "New File", "Enter filename:")
            if ok and filename:
                new_file_path = os.path.join(directory, filename)
                try:
                    with open(new_file_path, 'w') as f:
                        f.write("")
                    self.refresh_view()
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not create file: {str(e)}")

    def set_root_path(self, path):
        self.tree_view.setRootIndex(self.model.index(path))

    def get_current_path(self):
        return self.model.rootPath()


