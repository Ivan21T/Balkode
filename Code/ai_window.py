from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QHBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath

class ChatbotWindow(QDialog):
    def __init__(self, parent=None, ai_button=None):
        super().__init__(parent)

        self.ai_button = ai_button
        self.parent_window = parent

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(300, 350)

        self.update_position()

        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.update_position)
        self.position_timer.start(100)

        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            QFrame#mainFrame {
                background-color: #2d2d2d;
                border: 1px solid #ffffff;
                border-radius: 12px;
            }
            QTextEdit {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 8px;
                font-size: 11px;
                font-family: Arial;
            }
            QLineEdit {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 1px solid #0084ff;
            }
            QPushButton {
                background-color: #0084ff;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0073e6;
            }
        """)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("mainFrame")
        self.main_frame.setFixedSize(280, 320)

        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        header_layout = QHBoxLayout()
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                border-image: url(../Assets/Icons_Pages/close_btn.png) 0 0 0 0 stretch stretch;
                
            }
            QPushButton:hover {
                background-color: #888888;
                border-image: url(../Assets/Icons_Pages/close_btn.png) 0 0 0 0 stretch stretch;
            }
        """)
        self.close_btn.clicked.connect(self.hide)

        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)
        layout.addLayout(header_layout)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMaximumHeight(220)
        self.chat_history.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a message...")

        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedWidth(60)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)

        self.send_btn.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_frame)

        self.last_parent_pos = None
        if self.parent_window:
            self.last_parent_pos = self.parent_window.pos()

        self.add_welcome_message()

    def update_position(self):
        if self.ai_button and self.ai_button.isVisible():
            try:
                button_global_pos = self.ai_button.mapToGlobal(QPoint(0, 0))
                button_center_x = button_global_pos.x() + self.ai_button.width() // 2

                bubble_x = button_center_x - self.width() // 2
                bubble_y = button_global_pos.y() - self.height() + 10

                self.move(bubble_x, bubble_y)

                self.update()

            except Exception as e:
                print(f"Position update error: {e}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bubble_rect = self.main_frame.geometry()
        path = QPainterPath()
        path.addRoundedRect(bubble_rect, 12, 12)

        arrow_x = self.width() // 2

        if self.ai_button and self.ai_button.isVisible():
            try:
                button_global_pos = self.ai_button.mapToGlobal(QPoint(0, 0))
                button_center_x = button_global_pos.x() + self.ai_button.width() // 2

                button_local_x = button_center_x - self.geometry().x()

                arrow_x = max(30, min(button_local_x, self.width() - 30))
            except Exception as e:
                print(f"Arrow position error: {e}")

        arrow_width = 20
        arrow_height = 10
        arrow_top = bubble_rect.bottom()

        path.moveTo(arrow_x - arrow_width // 2, arrow_top)
        path.lineTo(arrow_x, arrow_top + arrow_height)
        path.lineTo(arrow_x + arrow_width // 2, arrow_top)
        path.lineTo(arrow_x - arrow_width // 2, arrow_top)

        painter.fillPath(path, QColor(45, 45, 45))

        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawPath(path)

    def showEvent(self, event):
        super().showEvent(event)
        self.update_position()
        self.input_box.setFocus()
        self.position_timer.start(100)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.position_timer.stop()

    def closeEvent(self, event):
        self.position_timer.stop()
        super().closeEvent(event)

    def add_welcome_message(self):
        welcome_msg = """
        <div style='text-align: center; color: #0084ff; margin: 10px 0;'>
            <b>AI Assistant</b><br>
            <span style='color: #888; font-size: 10px;'>How can I help?</span>
        </div>
        """
        self.chat_history.setHtml(welcome_msg)

    def send_message(self):
        text = self.input_box.text().strip()
        if not text:
            return

        self.add_user_message(text)
        self.input_box.clear()

        self.add_ai_thinking()

        QTimer.singleShot(800, lambda: self.add_ai_response(text))

    def add_user_message(self, text):
        user_html = f"""
        <div style='margin: 5px 0; text-align: right;'>
            <div style='display: inline-block; background: #0084ff; color: white; 
                        padding: 6px 10px; border-radius: 12px; font-size: 11px;
                        max-width: 80%; word-wrap: break-word;'>
                {text}
            </div>
        </div>
        """
        self.append_to_chat(user_html)

    def add_ai_thinking(self):
        thinking_html = """
        <div style='margin: 5px 0; text-align: left;'>
            <div style='display: inline-block; background: #404040; color: #aaa; 
                        padding: 6px 10px; border-radius: 12px; font-size: 11px;
                        font-style: italic;'>
                Thinking...
            </div>
        </div>
        """
        self.append_to_chat(thinking_html)

    def add_ai_response(self, user_text):
        current_text = self.chat_history.toHtml()
        current_text = current_text.replace("Thinking...", "")
        self.chat_history.setHtml(current_text)

        bot_reply = self.generate_response(user_text)

        ai_html = f"""
        <div style='margin: 5px 0; text-align: left;'>
            <div style='display: inline-block; background: #404040; color: white; 
                        padding: 6px 10px; border-radius: 12px; font-size: 11px;
                        max-width: 80%; word-wrap: break-word;'>
                {bot_reply}
            </div>
        </div>
        """
        self.append_to_chat(ai_html)

        self.chat_history.verticalScrollBar().setValue(
            self.chat_history.verticalScrollBar().maximum()
        )

    def generate_response(self, user_text):
        user_text_lower = user_text.lower()

        if "hello" in user_text_lower or "hi" in user_text:
            return "Hello! How can I help?"
        elif "explain" in user_text_lower:
            return "I can explain code. What do you need?"
        elif "error" in user_text_lower:
            return "Let me help with that error."
        elif "thank" in user_text_lower:
            return "You're welcome!"
        else:
            return "I understand. How can I assist?"

    def append_to_chat(self, html_content):
        current_html = self.chat_history.toHtml()
        new_html = current_html + html_content
        self.chat_history.setHtml(new_html)