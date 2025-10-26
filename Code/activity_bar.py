import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class IconBarButton(QPushButton):
    def __init__(self,icon_name,tooltip, parent=None):
        super().__init__(parent)
        self.setFixedSize(48,48)
        self.setToolTip(tooltip)
        self.setCheckable(True)
        self.setIcon(QIcon(icon_name))

        self.setStyleSheet("""
                    IconBarButton {
                        background: transparent;
                        border: none;
                        border-radius: 4px;
                        color: #858585;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    IconBarButton:hover {
                        background: #2a2d2e;
                        color: #cccccc;
                    }
                    IconBarButton:checked {
                        background: #37373d;
                        border-left: 2px solid #007acc;
                        color: #ffffff;
                    }
                """)
class ActivityBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(48)
        self.setStyleSheet("""
            ActivityBar {
                background: #333333;
                border: none;
                border-right: 1px solid #2d2d2d;
            }
        """)

