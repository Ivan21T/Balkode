from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json


class Settings(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        self.setStyleSheet("""
            Settings {
                background-color: #1a1d21;
                color: #e4e6eb;
                border: none;
                border-radius: 12px;
            }
            QLabel {
                color: #e4e6eb;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 5px;
            }
            QComboBox {
                background-color: #25282e;
                color: #e4e6eb;
                border: 1.5px solid #3a3d45;
                border-radius: 8px;
                padding: 10px 15px;
                min-width: 140px;
                font-size: 13px;
                font-weight: 500;
            }
            QComboBox:hover {
                border: 1.5px solid #4a4d55;
                background-color: #2a2d34;
            }
            QComboBox:focus {
                border: 1.5px solid #2d8cff;
                background-color: #25282e;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #8b8d92;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #25282e;
                color: #e4e6eb;
                border: 1.5px solid #3a3d45;
                border-radius: 8px;
                selection-background-color: #2d8cff;
                outline: none;
                padding: 5px;
                font-size: 13px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #2d8cff;
                color: #ffffff;
            }
            QCheckBox {
                color: #e4e6eb;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 5px;
                spacing: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1.5px solid #3a3d45;
                border-radius: 5px;
                background-color: #25282e;
            }
            QCheckBox::indicator:checked {
                background-color: #2d8cff;
                border: 1.5px solid #2d8cff;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #4da1ff;
                border: 1.5px solid #4da1ff;
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid #4a4d55;
                background-color: #2a2d34;
            }
            QCheckBox::indicator:checked:pressed {
                background-color: #1a7ae6;
                border: 1.5px solid #1a7ae6;
            }
        """)

        # Theme Section
        self.h1_layout = QHBoxLayout()
        self.theme = QLabel("Theme", self)
        self.theme_menu = QComboBox(self)
        self.theme_menu.addItems(["Dark", "Light", "Nord", "Blue", "Midnight"])
        self.theme_menu.setCurrentText("Dark")
        self.h1_layout.addWidget(self.theme)
        self.h1_layout.addWidget(self.theme_menu)
        self.h1_layout.addStretch()

        # Font Size Section
        self.h2_layout = QHBoxLayout()
        self.font_size_label = QLabel("Font Size", self)
        self.font_size_combo = QComboBox(self)
        self.font_size_combo.addItems(["10", "12", "14", "16", "18", "20", "24"])
        self.font_size_combo.setCurrentText("14")
        self.h2_layout.addWidget(self.font_size_label)
        self.h2_layout.addWidget(self.font_size_combo)
        self.h2_layout.addStretch()

        # Code Formatting Section
        self.h3_layout = QHBoxLayout()
        self.formatting_label = QLabel("Code Style", self)
        self.formatting_combo = QComboBox(self)
        self.formatting_combo.addItems(["K&R Style", "Allman Style", "GNU Style", "Whitesmiths Style", "Google Style"])
        self.formatting_combo.setCurrentText("K&R Style")
        self.h3_layout.addWidget(self.formatting_label)
        self.h3_layout.addWidget(self.formatting_combo)
        self.h3_layout.addStretch()

        # AI Section
        self.h4_layout = QHBoxLayout()
        self.ai_label = QLabel("AI Assistant", self)
        self.ai_toggle = QCheckBox("Enable AI Features", self)
        self.ai_toggle.setChecked(True)
        self.h4_layout.addWidget(self.ai_label)
        self.h4_layout.addWidget(self.ai_toggle)
        self.h4_layout.addStretch()

        # Add all sections to main layout
        main_layout.addLayout(self.h1_layout)
        main_layout.addLayout(self.h2_layout)
        main_layout.addLayout(self.h3_layout)
        main_layout.addLayout(self.h4_layout)

        # Add stretch to push content to top
        main_layout.addStretch()

        # Set modern spacing and margins
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

    def get_settings(self):
        """Get current settings as a dictionary"""
        return {
            "theme": self.theme_menu.currentText(),
            "font_size": self.font_size_combo.currentText(),
            "code_style": self.formatting_combo.currentText(),
            "ai_enabled": self.ai_toggle.isChecked()
        }

    def set_settings(self, theme="Dark", font_size="14", code_style="K&R Style", ai_enabled=True):
        """Set settings from values"""
        self.theme_menu.setCurrentText(theme)
        self.font_size_combo.setCurrentText(font_size)
        self.formatting_combo.setCurrentText(code_style)
        self.ai_toggle.setChecked(ai_enabled)


class SettingsTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings Panel Preview")
        self.setGeometry(200, 200, 500, 450)

        # Apply modern dark theme to the entire app
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #0f1419, stop: 1 #1a1f24);
            }
            QPushButton {
                background-color: #25282e;
                color: #e4e6eb;
                border: 1.5px solid #3a3d45;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2a2d34;
                border: 1.5px solid #4a4d55;
            }
            QPushButton:pressed {
                background-color: #1e2126;
            }
            QPushButton:focus {
                border: 1.5px solid #2d8cff;
            }
            QPushButton#primary {
                background-color: #2d8cff;
                color: #ffffff;
                border: 1.5px solid #2d8cff;
            }
            QPushButton#primary:hover {
                background-color: #4da1ff;
                border: 1.5px solid #4da1ff;
            }
            QPushButton#primary:pressed {
                background-color: #1a7ae6;
                border: 1.5px solid #1a7ae6;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: 700;
                color: #ffffff;
                padding: 10px 0px;
            }
            QLabel#subtitle {
                font-size: 14px;
                color: #8b8d92;
                padding: 0px 0px 10px 0px;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with center alignment
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Header section - centered
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Settings Preview")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("This is how your Settings panel will look")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Settings panel - centered
        self.settings_panel = Settings()
        self.settings_panel.setup_ui()
        main_layout.addWidget(self.settings_panel, alignment=Qt.AlignCenter)

        # Centered button layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(20)

        self.confirm_btn = QPushButton("Confirm Settings")
        self.confirm_btn.setObjectName("primary")
        self.confirm_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_btn.clicked.connect(self.confirm_settings)

        button_layout.addWidget(self.confirm_btn)
        main_layout.addLayout(button_layout)

    def confirm_settings(self):
        """Show confirmation with current settings"""
        settings = self.settings_panel.get_settings()

        message = f"""Settings have been saved successfully."""

        msg = QMessageBox(self)
        msg.setWindowTitle("Settings Confirmed")
        msg.setTextFormat(Qt.RichText)
        msg.setText(message.strip())
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1a1d21;
                color: #e4e6eb;
            }
            QMessageBox QLabel {
                color: #e4e6eb;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #2d8cff;
                color: #ffffff;
                border: 1.5px solid #2d8cff;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4da1ff;
            }
        """)
        msg.exec()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Set modern font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show the test window
    window = SettingsTestApp()
    window.show()

    sys.exit(app.exec())