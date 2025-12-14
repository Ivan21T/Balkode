from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys


class Settings(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(40, 40, 40, 60)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        self.setStyleSheet("""
            QFrame { background: #1a1d23; }
            QLabel { color: #e4e6eb; font-size: 14px; }
            QLabel#header { font-size: 20px; font-weight: bold; color: white; }
            QLineEdit {
                background: #2a2e35; color: white; border: 1px solid #3a3f47;
                border-radius: 8px; padding: 12px 15px; font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #2d8cff; }
            QLineEdit[readOnly="true"] { background: #25282e; color: #a0a2a7; }
            QPushButton {
                background: #2d8cff; color: white; border: none;
                border-radius: 8px; padding: 12px 24px; font-weight: bold;
            }
            QPushButton:hover { background: #4da1ff; }
            QPushButton:pressed { background: #1a7ae6; }
            QPushButton#cancel {
                background: transparent; color: #e4e6eb; border: 1px solid #3a3f47;
            }
            QPushButton#cancel:hover { background: #2a2e35; }

            QComboBox {
                background: #2a2e35;
                color: white;
                border: 1px solid #3a3f47;
                border-radius: 8px;
                padding: 12px 40px 12px 15px;
                font-size: 14px;
            }
            QComboBox:focus { border: 1px solid #2d8cff; }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 40px;
                background: #2d8cff;
                border-radius: 0px 8px 8px 0px;
            }
            QComboBox::down-arrow {
                image: url(../Assets/Icons_Pages/arrow_down.png);
            }
            QComboBox::down-arrow:on,
            QComboBox::up-arrow {
                image: url(../Assets/Icons_Pages/arrow_up.png);
            }

            QCheckBox { color: white; spacing: 10px; font-size: 14px; }
            QCheckBox::indicator {
                width: 20px; height: 20px; border-radius: 5px;
                border: 2px solid #3a3f47; background: #2a2e35;
            }
            QCheckBox::indicator:checked { background: #2d8cff; border-color: #2d8cff; }
            QTextEdit#codePreview {
                background: #1e2228; color: #e4e6eb; border: 1px solid #3a3f47;
                border-radius: 8px; padding: 15px; font-family: 'Courier New', monospace;
                font-size: 13px; line-height: 1.4;
            }
            QTextEdit#codePreview:focus { border: 1px solid #2d8cff; }
            QScrollBar:vertical { background: transparent; width: 8px; }
            QScrollBar::handle:vertical {
                background: #2d8cff; border-radius: 4px; min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { background: #4da1ff; }
        """)

        self.setup_ui()
        self.update_code_preview()

    def setup_ui(self):
        title = QLabel("Settings")
        title.setObjectName("header")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        subtitle = QLabel("Customize your development environment")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #8b8d92; font-size: 14px; margin-bottom: 10px;")
        self.layout.addWidget(subtitle)

        profile_header = QLabel("Profile")
        profile_header.setObjectName("header")
        self.layout.addWidget(profile_header)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit("John Doe")
        self.name_edit.setReadOnly(True)
        name_layout.addWidget(self.name_edit)
        form_layout.addLayout(name_layout)

        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email:"))
        self.email_edit = QLineEdit("john.doe@example.com")
        self.email_edit.setReadOnly(True)
        email_layout.addWidget(self.email_edit)
        form_layout.addLayout(email_layout)

        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password:"))
        self.password_edit = QLineEdit("••••••••")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setReadOnly(True)
        password_layout.addWidget(self.password_edit)
        form_layout.addLayout(password_layout)

        self.layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit Profile")
        self.edit_btn.clicked.connect(self.toggle_edit)
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel")
        self.save_btn.clicked.connect(self.save_changes)
        self.cancel_btn.clicked.connect(self.cancel_edit)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.save_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.layout.addLayout(btn_layout)
        self.add_section_line()

        pref_header = QLabel("Appearance")
        pref_header.setObjectName("header")
        self.layout.addWidget(pref_header)

        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(15)

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Nord", "Dracula", "Solarized"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        settings_layout.addLayout(theme_layout)

        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(["12px", "14px", "16px", "18px"])
        self.font_combo.setCurrentText("14px")
        font_layout.addWidget(self.font_combo)
        font_layout.addStretch()
        settings_layout.addLayout(font_layout)

        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Spanish", "French", "German", "Japanese"])
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        settings_layout.addLayout(lang_layout)

        self.layout.addLayout(settings_layout)
        self.add_section_line()

        code_header = QLabel("Coding Style")
        code_header.setObjectName("header")
        self.layout.addWidget(code_header)

        code_layout = QVBoxLayout()
        code_layout.setSpacing(15)

        code_style_layout = QHBoxLayout()
        code_style_layout.addWidget(QLabel("Brace Style:"))
        self.code_style_combo = QComboBox()
        self.code_style_combo.addItems(["K&R", "Allman", "1TBS", "Stroustrup", "Whitesmiths"])
        self.code_style_combo.currentTextChanged.connect(self.update_code_preview)
        code_style_layout.addWidget(self.code_style_combo)
        code_style_layout.addStretch()
        code_layout.addLayout(code_style_layout)

        indent_layout = QHBoxLayout()
        indent_layout.addWidget(QLabel("Indentation:"))
        self.indent_combo = QComboBox()
        self.indent_combo.addItems(["Spaces (4)", "Tabs", "Spaces (2)", "Spaces (8)"])
        self.indent_combo.currentTextChanged.connect(self.update_code_preview)
        indent_layout.addWidget(self.indent_combo)
        indent_layout.addStretch()
        code_layout.addLayout(indent_layout)

        preview_label = QLabel("Code Style Preview:")
        preview_label.setStyleSheet("color: #e4e6eb; font-size: 14px; font-weight: bold;")
        code_layout.addWidget(preview_label)

        self.code_preview = QTextEdit()
        self.code_preview.setObjectName("codePreview")
        self.code_preview.setMinimumHeight(200)
        self.code_preview.setReadOnly(True)
        code_layout.addWidget(self.code_preview)

        self.layout.addLayout(code_layout)

        ai_layout = QHBoxLayout()
        self.ai_toggle = QCheckBox("Enable AI Code Assistant")
        self.ai_toggle.setChecked(True)
        self.ai_toggle.toggled.connect(self.on_ai_toggled)
        ai_layout.addWidget(self.ai_toggle)
        ai_layout.addStretch()
        self.layout.addLayout(ai_layout)

        self.layout.addStretch()

        apply_btn = QPushButton("Save All Settings")
        apply_btn.setFixedHeight(45)
        apply_btn.clicked.connect(self.apply_settings)
        self.layout.addWidget(apply_btn)

        self.original_name = "John Doe"
        self.original_email = "john.doe@example.com"

    def add_section_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: #3a3f47; margin: 20px 0;")
        self.layout.addWidget(line)

    def update_code_preview(self):
        style = self.code_style_combo.currentText()
        indent = self.indent_combo.currentText()
        if "Spaces (2)" in indent:
            indent_size = 2;
            indent_char = " "
        elif "Spaces (8)" in indent:
            indent_size = 8;
            indent_char = " "
        elif "Tabs" in indent:
            indent_size = 1;
            indent_char = "\t"
        else:
            indent_size = 4;
            indent_char = " "
        indent1 = indent_char * indent_size
        indent2 = indent_char * (indent_size * 2)
        indent3 = indent_char * (indent_size * 3)

        if style == "K&R":
            code = f"""void example() {{
{indent1}if (condition) {{
{indent2}doSomething();
{indent2}for (int i = 0; i < 10; i++) {{
{indent3}process(i);
{indent2}}}
{indent1}}}
}}"""
        elif style == "Allman":
            code = f"""void example()
{{
{indent1}if (condition)
{indent1}{{
{indent2}doSomething();
{indent2}for (int i = 0; i < 10; i++)
{indent2}{{
{indent3}process(i);
{indent2}}}
{indent1}}}
}}"""
        elif style == "1TBS":
            code = f"""void example() {{
{indent1}if (condition) {{
{indent2}doSomething();
{indent1}}} else {{
{indent2}doSomethingElse();
{indent1}}}
{indent1}for (int i = 0; i < 10; i++) {{
{indent2}process(i);
{indent1}}}
}}"""
        elif style == "Stroustrup":
            code = f"""void example()
{{
{indent1}if (condition) {{
{indent2}doSomething();
{indent1}}}
{indent1}else {{
{indent2}doSomethingElse();
{indent1}}}
{indent1}for (int i = 0; i < 10; i++) {{
{indent2}process(i);
{indent1}}}
}}"""
        else:
            code = f"""void example()
    {{
{indent1}if (condition)
{indent1}    {{
{indent2}doSomething();
{indent1}    }}
{indent1}for (int i = 0; i < 10; i++)
{indent1}    {{
{indent2}process(i);
{indent1}    }}
    }}"""
        self.code_preview.setPlainText(code)

    def on_ai_toggled(self, checked):
        print(f"AI Code Assistant {'enabled' if checked else 'disabled'}")

    def toggle_edit(self):
        editing = not self.name_edit.isReadOnly()
        self.name_edit.setReadOnly(editing)
        self.email_edit.setReadOnly(editing)
        self.password_edit.setReadOnly(editing)
        self.password_edit.setEchoMode(QLineEdit.Normal if not editing else QLineEdit.Password)
        self.password_edit.setText("" if not editing else "••••••••")
        self.edit_btn.setVisible(editing)
        self.save_btn.setVisible(not editing)
        self.cancel_btn.setVisible(not editing)

    def save_changes(self):
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        if not name or "@" not in email:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid name and email.")
            return
        self.original_name = name
        self.original_email = email
        QMessageBox.information(self, "Success", "Profile updated!")
        self.toggle_edit()

    def cancel_edit(self):
        self.name_edit.setText(self.original_name)
        self.email_edit.setText(self.original_email)
        self.password_edit.setText("••••••••")
        self.toggle_edit()

    def apply_settings(self):
        settings = {
            "theme": self.theme_combo.currentText(),
            "font_size": self.font_combo.currentText(),
            "language": self.lang_combo.currentText(),
            "brace_style": self.code_style_combo.currentText(),
            "indentation": self.indent_combo.currentText(),
            "ai_enabled": self.ai_toggle.isChecked()
        }
        message = f"""Settings Saved Successfully!

Appearance:
• Theme: {settings['theme']}
• Font Size: {settings['font_size']}
• Language: {settings['language']}

Coding Style:
• Brace Style: {settings['brace_style']}
• Indentation: {settings['indentation']}
• AI Assistant: {'Enabled' if settings['ai_enabled'] else 'Disabled'}"""
        QMessageBox.information(self, "Settings Saved", message)


