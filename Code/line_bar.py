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

class LineBar(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_bar_width(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor("#1e1e1e"))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()

        top = int(
            self.editor.blockBoundingGeometry(block)
            .translated(self.editor.contentOffset())
            .top()
        )
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)

                painter.setPen(QColor("#858585"))
                painter.drawText(
                    0,
                    top,
                    self.width() - 6,
                    self.editor.fontMetrics().height(),
                    Qt.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            block_number += 1
