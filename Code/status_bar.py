import psutil
from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import QTimer


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.time=QLabel("00:00")
        self.cursor_label = QLabel("Ln 1, Col 1")
        self.separator1 = QLabel("|")
        self.cpu_label = QLabel("CPU: 0%")
        self.separator2 = QLabel("|")
        self.memory_label = QLabel("RAM: 0%")

        self.addWidget(self.time)
        self.addPermanentWidget(self.cursor_label)
        self.addPermanentWidget(self.separator1)
        self.addPermanentWidget(self.cpu_label)
        self.addPermanentWidget(self.separator2)
        self.addPermanentWidget(self.memory_label)

        self.setStyleSheet("""
            QStatusBar {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
                margin: 0 6px;
            }
            QLabel#cpu_normal {
                color: #4CAF50;  
            }
            QLabel#cpu_warning {
                color: #FF9800;  
            }
            QLabel#cpu_critical {
                color: #F44336;  
            }
            QLabel#ram_normal {
                color: #4CAF50;  
            }
            QLabel#ram_warning {
                color: #FF9800;  
            }
            QLabel#ram_critical {
                color: #F44336;  
            }
        """)


        self.cpu_label.setObjectName("cpu_normal")
        self.memory_label.setObjectName("ram_normal")


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_usage)
        self.timer.start(1000)
        self.update_system_usage()

    def update_system_usage(self):
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent

        self.cpu_label.setText(f"CPU: {cpu:.0f}%")
        if cpu > 80:
            self.cpu_label.setObjectName("cpu_critical")
        elif cpu > 60:
            self.cpu_label.setObjectName("cpu_warning")
        else:
            self.cpu_label.setObjectName("cpu_normal")

        self.memory_label.setText(f"RAM: {mem:.0f}%")
        if mem > 85:
            self.memory_label.setObjectName("ram_critical")
        elif mem > 70:
            self.memory_label.setObjectName("ram_warning")
        else:
            self.memory_label.setObjectName("ram_normal")

        self.cpu_label.style().unpolish(self.cpu_label)
        self.cpu_label.style().polish(self.cpu_label)
        self.memory_label.style().unpolish(self.memory_label)
        self.memory_label.style().polish(self.memory_label)

    def update_cursor_position(self, line, col):
        self.cursor_label.setText(f"Ln {line}, Col {col}")

