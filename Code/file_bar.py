import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class FileBar(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        self.setStyleSheet("""
                    QTabWidget::pane {
                        border: none;
                        background: transparent;
                        margin: 0px;
                        padding: 0px;
                    }

                    QTabBar {
                        border: none;
                        background: transparent;
                    }

                     QTabBar::tab {
                        background: #363636;
                        color: #cccccc;
                        padding: 8px 24px 8px 16px;  
                        margin-right: 4px;
                        border: 1px solid transparent;
                        font-weight: 500;
                        min-width: 120px;
                        border-radius: 6px;
                        margin-top: 4px;
                        margin-bottom: 2px;
                    }

                    QTabBar::tab:selected {
                        background: #363636;
                        color: #ffffff;
                        border: 1px solid #007acc;
                        margin-top: 0px;
                        margin-bottom: 0px;
                        margin-right: 6px;
                    }

                    QTabBar::tab:!selected {
                        background: #363636;
                        margin-right: 6px;
                    }

                    QTabBar::tab:hover {
                        background: #3e3e42;
                        margin-right: 6px;
                    }

                    QTabBar::tab:selected:hover {
                        background: #363636;
                        border: 1px solid #007acc;
                        margin-right: 6px;
                    }

                    QTabBar::close-button {
                        margin-right: 8px;
                    }

                    QTabBar::tab:!selected QTabBar::close-button {
                        width: 0px;
                        height: 0px;
                        margin: 0px;
                        padding: 0px;
                    }
                """)

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
                # Emit save signal if needed
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

