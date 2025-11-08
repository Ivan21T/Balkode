from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMenuBar {
                background-color: #222;
                color: white;
                spacing: 6px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 6px 12px;
            }
            QMenuBar::item:selected {
                background: #0078d7;
                border-radius: 4px;
            }

            QMenu {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444;
            }
            QMenu::item {
                padding: 6px 26px;  
            }
            QMenu::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #555;
                margin: 4px 8px;
            }

            QMenu::indicator {
                width: 10px;
                height: 10px;
                border-radius: 5px;       
                border: 2px solid #0078d7;
                margin-left: 6px;
                background: transparent;
            }

            QMenu::indicator:checked {
                background-color: #0078d7;
                border: 2px solid #0078d7;
            }

            QMenu::indicator:unchecked {
                background: transparent;
                border: 2px solid #0078d7;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        # The menus
        self.file_menu = self.addMenu("File")
        self.edit_menu = self.addMenu("Edit")
        self.help_menu = self.addMenu("Help")
        self.about_menu = self.addMenu("About")

        # The file menu options
        self.new_text_file = self.file_menu.addAction("New Text File")
        self.new_text_file.setShortcut("Ctrl+N")

        self.new_file = self.file_menu.addAction("New File")
        self.new_file.setShortcut("Ctrl+Shift+N")

        self.file_menu.addSeparator()

        self.open_file = self.file_menu.addAction("Open File")
        self.open_file.setShortcut("Ctrl+O")

        self.open_folder = self.file_menu.addAction("Open Folder")
        self.open_folder.setShortcut("Ctrl+K")

        self.file_menu.addSeparator()

        self.save_file = self.file_menu.addAction("Save File")
        self.save_file.setShortcut("Ctrl+S")

        self.save_as = self.file_menu.addAction("Save As...")
        self.save_as.setShortcut("Ctrl+Shift+S")

        self.auto_save = self.file_menu.addAction("Auto Save")
        self.auto_save.setCheckable(True)
        self.auto_save.setShortcut("Ctrl+Alt+S")

        self.file_menu.addSeparator()

        self.close_editor = self.file_menu.addAction("Close Editor")
        self.close_editor.setShortcut("Ctrl+W")

        self.close_folder = self.file_menu.addAction("Close Folder")
        self.close_folder.setShortcut("Ctrl+Shift+W")

        self.close_window = self.file_menu.addAction("Close Window")
        self.close_window.setShortcut("Alt+F4")

        self.file_menu.addSeparator()

        self.exit = self.file_menu.addAction("Exit")
        self.exit.setShortcut("Ctrl+Q")

        #The edit menu options
        self.undo = self.edit_menu.addAction("Undo")
        self.undo.setShortcut("Ctrl+Z")

        self.redo = self.edit_menu.addAction("Redo")
        self.redo.setShortcut("Ctrl+Y")

        self.edit_menu.addSeparator()

        self.cut = self.edit_menu.addAction("Cut")
        self.cut.setShortcut("Ctrl+X")

        self.copy = self.edit_menu.addAction("Copy")
        self.copy.setShortcut("Ctrl+C")

        self.paste = self.edit_menu.addAction("Paste")
        self.paste.setShortcut("Ctrl+V")

        self.edit_menu.addSeparator()

        self.find = self.edit_menu.addAction("Find")
        self.find.setShortcut("Ctrl+F")

        self.replace = self.edit_menu.addAction("Replace")
        self.replace.setShortcut("Ctrl+R")




