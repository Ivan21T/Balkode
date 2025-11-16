import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from observer import Observer
import json

with open("settings.json", "r") as file:
    settings_json=json.load(file)
activity_bar_style=""
icon_style=""
if settings_json["settings"][0]["theme"]=="Dark":
    for style in settings_json["styles"]["dark"]:
        if style["name"]=="icon":
            icon_style=style["style"]
        elif style["name"]=="activity_bar":
            activity_bar_style=style["style"]
else:
    print("There is no code for light theme")


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
observer=Observer()
class IconBarButton(QPushButton):
    def __init__(self, icon_path, tooltip, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 48)
        self.setToolTip(tooltip)
        self.setCheckable(True)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(24, 24))

        self.setStyleSheet(icon_style)


class ActivityBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(48)
        self.setStyleSheet(activity_bar_style)

        self.current_activity = None
        self.setup_activity_bar()
        observer.value = self.current_activity

    def setup_activity_bar(self):
        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        activities = [
            (os.path.join(base_dir, "Assets", "ActivityBar_Icons", "explorer.png"), "Explorer"),
            (os.path.join(base_dir, "Assets", "ActivityBar_Icons", "search.png"), "Search"),
            (os.path.join(base_dir, "Assets", "ActivityBar_Icons", "debug.png"), "Debug"),
            (os.path.join(base_dir, "Assets", "ActivityBar_Icons", "terminal.png"), "Terminal")
        ]

        for icon_path, tooltip in activities:
            btn = IconBarButton(icon_path, tooltip)
            btn.activity_name = tooltip
            btn.toggled.connect(self.on_button_toggled)
            layout.addWidget(btn)

        layout.addStretch()


        settings_path = os.path.join(base_dir, "Assets", "ActivityBar_Icons", "settings.png")
        settings_btn = IconBarButton(settings_path, "Settings")
        settings_btn.activity_name = "Settings"
        settings_btn.toggled.connect(self.on_button_toggled)
        layout.addWidget(settings_btn)

        self.setLayout(layout)


    def on_button_toggled(self, checked):
        sender_btn = self.sender()

        if checked:
            for btn in self.findChildren(IconBarButton):
                if btn != sender_btn:
                    btn.setChecked(False)

            self.current_activity = sender_btn.activity_name
            observer.value = self.current_activity

        else:
            self.current_activity = None
            observer.value = self.current_activity