from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json


with open("settings.json", "r") as file:
    style_settings = json.load(file)

line_bar_style=""
number_style=""
number_highlight=""

if style_settings["settings"][0]["theme"]=="Dark":
    for style_setting in style_settings["styles"]["dark"]:
        if style_setting["name"] == "line_bar":
            line_bar_style = style_setting["style"]
            number_style = style_setting["number_normal"]
            number_highlight = style_setting["number_highlight"]
            break
else:
    #Here is the logic for the light theme
    print("There is no light theme setting")

class LineBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(30)
        self.setStyleSheet(line_bar_style)
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
        number_label.setStyleSheet(number_style)
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
                    widget.setStyleSheet(number_highlight)
                else:
                    widget.setStyleSheet(number_style)