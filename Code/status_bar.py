import psutil
import time
from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import QTimer, QDateTime


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.time_label = QLabel("00:00:00")
        self.cursor_label = QLabel("Ln 1, Col 1")
        self.separator1 = QLabel("|")
        self.cpu_label = QLabel("CPU: 0%")
        self.separator2 = QLabel("|")
        self.memory_label = QLabel("RAM: 0%")

        self.addWidget(self.time_label)
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
        """)

        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.update_system_usage)
        self.system_timer.start(1000)
        self.update_system_usage()

        self.coding_timer = QTimer()
        self.coding_timer.timeout.connect(self.update_timer)
        self.elapsed_seconds = 0
        self.coding_timer.start(1000)

    def get_percentage_color(self, percent):
        if percent <= 50:
            return "#00ff00"
        elif percent <= 80:
            return "#ffa500"
        else:
            return "#ff0000"

    def update_system_usage(self):
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent

        cpu_color = self.get_percentage_color(cpu)
        mem_color = self.get_percentage_color(mem)


        self.cpu_label.setText(f'<font color="{cpu_color}">CPU: {cpu:.0f}%</font>')
        self.memory_label.setText(f'<font color="{mem_color}">RAM: {mem:.0f}%</font>')

    def update_cursor_position(self, line, col):
        self.cursor_label.setText(f"Ln {line}, Col {col}")

    def update_timer(self):
        self.elapsed_seconds += 1

        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60

        self.time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
