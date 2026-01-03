from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from line_bar import*
import json

with open("settings.json", "r") as file:
    style_settings = json.load(file)

code_editor_style=""
if style_settings["settings"][0]["theme"]=="Dark":
    for style in style_settings["styles"]["dark"]:
        if style["name"]=="code_editor":
            code_editor_style = style["style"]
            break
else:
    print("There is no code for light theme")

class CodeEdit(QPlainTextEdit):
    def __init__(self, line_bar):
        super().__init__()

        self.line_bar = line_bar
        self.line_bar.editor = self

        self.blockCountChanged.connect(self.update_line_bar_width)
        self.updateRequest.connect(self.update_line_bar)
        self.cursorPositionChanged.connect(self.update_line_bar)

        self.update_line_bar_width(0)

    def line_bar_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance("9") * digits

    def update_line_bar_width(self, _):
        self.setViewportMargins(self.line_bar_width(), 0, 0, 0)

    def update_line_bar(self, rect=None, dy=0):
        if dy:
            self.line_bar.scroll(0, dy)
        else:
            self.line_bar.update()

        if rect and rect.contains(self.viewport().rect()):
            self.update_line_bar_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_bar.setGeometry(
            QRect(cr.left(), cr.top(), self.line_bar_width(), cr.height())
        )


