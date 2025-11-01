from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os
import platform


class TerminalFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Simple styling
        self.setStyleSheet("""
            TerminalFrame {
                background: #1e1e1e;
                border-top: 1px solid #3e3e42;
            }
            QTextEdit {
                background: #1e1e1e;
                color: #cccccc;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 12px;
                border: none;
                selection-background-color: #264f78;
            }
            QLineEdit {
                background: #252526;
                color: #00ff00;
                border: none;
                border-top: 1px solid #3e3e42;
                padding: 8px;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 12px;
            }
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4a4a4a;
            }
        """)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Terminal output with colored text support
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Terminal input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type commands here...")
        self.input.returnPressed.connect(self.run_command)

        # Add widgets
        layout.addWidget(self.output)
        layout.addWidget(self.input)

        # Make terminal resizable
        self.setMinimumHeight(100)
        self.setMaximumHeight(1000)  # Allow growing up to 1000px

        # Start shell
        self.start_shell()

    def start_shell(self):
        # Create process
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)

        # Setup shell based on OS
        if platform.system() == "Windows":
            self.process.start("cmd.exe")
        else:
            # Set up colored terminal for Unix
            env = QProcessEnvironment.systemEnvironment()
            env.insert("TERM", "xterm-256color")
            env.insert("CLICOLOR", "1")
            env.insert("FORCE_COLOR", "1")
            self.process.setProcessEnvironment(env)
            self.process.start("/bin/bash")

    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        self.append_colored_text(data)

    def read_error(self):
        data = self.process.readAllStandardError().data().decode('utf-8', errors='ignore')
        self.append_colored_text(data, color="#ff6b6b")  # Red color for errors

    def append_colored_text(self, text, color=None):
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)

        if color:
            # Apply color formatting
            format = QTextCharFormat()
            format.setForeground(QColor(color))
            cursor.setCharFormat(format)

        cursor.insertText(text)

        # Scroll to bottom
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()

    def run_command(self):
        command = self.input.text() + "\n"

        # Display the command in terminal (green color)
        self.append_colored_text(f"$ {command}", color="#00ff00")
        self.input.clear()

        if self.process.state() == QProcess.Running:
            self.process.write(command.encode())

    # Resize methods
    def expand(self):
        """Make terminal bigger"""
        current_height = self.height()
        self.setMinimumHeight(current_height + 100)

    def shrink(self):
        """Make terminal smaller"""
        current_height = self.height()
        if current_height > 100:
            self.setMinimumHeight(current_height - 100)

    def set_height(self, height):
        """Set specific height"""
        self.setFixedHeight(height)

    def toggle_size(self):
        """Toggle between small and large"""
        if self.height() <= 150:
            self.setFixedHeight(400)
        else:
            self.setFixedHeight(150)

    def close_terminal(self):
        """Quick close terminal"""
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
        self.hide()

    def clear_terminal(self):
        """Clear terminal output"""
        self.output.clear()