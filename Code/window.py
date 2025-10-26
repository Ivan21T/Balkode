from PySide6.QtWidgets import QMainWindow, QVBoxLayout
import activity_bar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Balkode")
        self.resize(800, 600)
        self.setupUi()


    def setupUi(self):
        layout_activityBar = QVBoxLayout()
        layout_activityBar.setSpacing(4)
        layout_activityBar.setContentsMargins(0,8,0,8)



