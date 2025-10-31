import sys
import os
import window
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Code.activity_bar import base_dir

app = QApplication()

app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(30, 30, 30))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
palette.setColor(QPalette.HighlightedText, Qt.black)

app.setPalette(palette)
app.setWindowIcon(QIcon(os.path.join(base_dir,"Assets","balkode.png")))

window = window.MainWindow()
window.show()
app.exec()