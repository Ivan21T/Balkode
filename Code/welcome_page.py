import os.path
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
)
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize
from activity_bar import base_dir

class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Balkode - Welcome")
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #1E1E1E;
                border: 1px solid #2E2E2E;
                border-radius: 10px;
                padding: 10px 20px;
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #232323;
                border: 1px solid #00aaff;
            }
            QPushButton:pressed {
                background-color: #0077cc;
                color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        layout.insertSpacing(1, 5)

        logo_label = QLabel()
        logo_label.setStyleSheet("background-color: transparent;")
        pixmap = QPixmap(os.path.join(base_dir,"Assets","welcome_icon.png"))
        pixmap = pixmap.scaled(QSize(250, 250),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        open_file_btn = QPushButton(QIcon(os.path.join(base_dir,"Assets","WelcomePage_Icons","file.png"))
                                    ," Open File")
        open_folder_btn = QPushButton(QIcon(os.path.join(base_dir,"Assets","WelcomePage_Icons","folder.png"))
                                    ," Open Folder")

        open_file_btn.clicked.connect(self.open_file)
        open_folder_btn.clicked.connect(self.open_folder)

        layout.addWidget(open_file_btn)
        layout.addWidget(open_folder_btn)

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file:
            print(f"Selected file: {file}")

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder:
            print(f"Selected folder: {folder}")



