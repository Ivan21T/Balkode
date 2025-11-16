import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import json

with open("settings.json", "r") as file:
    style_settings = json.load(file)
file_bar_style = ""
if style_settings["settings"][0]["theme"]=="Dark":
    for style_entry in style_settings["styles"]["dark"]:
        if style_entry["name"] == "file_bar":
            file_bar_style = style_entry["style"]
            break
else:
    print("No light theme")


class FileBar(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        self.setStyleSheet(file_bar_style)

        self.tabCloseRequested.connect(self.close_tab)

    def add_tab(self, title, widget):
        index = self.addTab(widget, title)
        self.setCurrentIndex(index)
        return index

    def close_tab(self, index):
        if self.tabText(index).endswith(' *'):
            reply = QMessageBox.question(
                self, "Save Changes?",
                f"Save changes to {self.tabText(index).replace(' *', '')}?",
                QMessageBox.Save | QMessageBox.Cancel
            )

            if reply == QMessageBox.Cancel:
                return
            elif reply == QMessageBox.Save:
                pass

        self.removeTab(index)

    def mark_modified(self, index, modified=True):
        text = self.tabText(index).replace(' *', '')
        self.setTabText(index, text + (' *' if modified else ''))

    def set_tab_title(self, index, title):
        current_text = self.tabText(index)
        if current_text.endswith(' *'):
            self.setTabText(index, title + ' *')
        else:
            self.setTabText(index, title)


