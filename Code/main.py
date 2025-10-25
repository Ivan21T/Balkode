import sys
import os
import window
from PySide6.QtWidgets import QApplication


app = QApplication()
window = window.MainWindow()
window.show()
app.exec()