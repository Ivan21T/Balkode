import os.path
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
)
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize
from activity_bar import base_dir
import json

with open("settings.json", "r") as file:
    style_setting = json.load(file)

welcome_page_style = ""
if style_setting["settings"][0]["theme"]=="Dark":
    for style_entry in style_setting["styles"]["dark"]:
        if style_entry["name"] == "welcome_page":
            welcome_page_style = style_entry["style"]
            break
else:
    print("I do not have light theme")

class WelcomePage(QWidget):
    def __init__(self,code_area_widget,code_area, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Balkode - Welcome")
        self.setStyleSheet(welcome_page_style)
        self.code_area_widget = code_area_widget
        self.code_area =code_area

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
        create_file_btn = QPushButton(QIcon(os.path.join(base_dir,"Assets","WelcomePage_Icons","create_file.png"))
                                      ," Create File")

        open_file_btn.clicked.connect(self.open_file)
        open_folder_btn.clicked.connect(self.open_folder)

        layout.addWidget(open_file_btn)
        layout.addWidget(open_folder_btn)
        layout.addWidget(create_file_btn)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*)"
        )
        if file_path:
                with open(file_path, "rb") as f:
                    data = f.read()
                    text = data.decode("utf-8")
                self.code_area.setPlainText(text)
                self.hide()
                self.code_area_widget.show()


    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder:
            print(f"Selected folder: {folder}")

    def create_file(self,code_area):
        return



