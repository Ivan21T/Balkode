from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class SearchFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(220)  # More compact width
        self.setStyleSheet("""
            SearchBar {
                background: #252526;
                border: none;
                border-left: 1px solid #3e3e42;
            }
            QLineEdit {
                background: #3c3c3c;
                border: 1px solid #0078d4;
                border-radius: 2px;
                padding: 2px 6px;
                color: #cccccc;
                font-size: 11px;
                selection-background-color: #0078d4;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            QPushButton {
                background: #0e639c;
                border: none;
                border-radius: 2px;
                color: white;
                padding: 3px 8px;
                font-size: 11px;
                font-weight: normal;
                min-height: 18px;
            }
            QPushButton:hover {
                background: #1177bb;
            }
            QPushButton:pressed {
                background: #0c547d;
            }
            QPushButton:disabled {
                background: #424242;
                color: #6e6e6e;
            }
            QLabel {
                color: #cccccc;
                font-size: 11px;
                font-weight: normal;
            }
            QCheckBox {
                color: #cccccc;
                font-size: 11px;
                spacing: 3px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #6e6e6e;
                background: #3c3c3c;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #0078d4;
                background: #0078d4;
            }
        """)

        # Main layout - vertical
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)  # Reduced margins
        layout.setSpacing(6)  # Reduced spacing

        # Find section
        find_layout = QHBoxLayout()
        find_layout.setSpacing(4)

        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find")
        self.find_input.setClearButtonEnabled(True)
        self.find_input.setFixedHeight(22)  # Smaller height

        self.find_prev_btn = QPushButton("▲")
        self.find_prev_btn.setFixedSize(20, 20)  # Smaller buttons
        self.find_prev_btn.setToolTip("Previous match")

        self.find_next_btn = QPushButton("▼")
        self.find_next_btn.setFixedSize(20, 20)
        self.find_next_btn.setToolTip("Next match")

        find_layout.addWidget(self.find_input)
        find_layout.addWidget(self.find_prev_btn)
        self.find_prev_btn.setFixedSize(20, 20)
        find_layout.addWidget(self.find_next_btn)
        self.find_next_btn.setFixedSize(20, 20)

        # Replace section
        replace_layout = QHBoxLayout()
        replace_layout.setSpacing(4)

        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace")
        self.replace_input.setClearButtonEnabled(True)
        self.replace_input.setFixedHeight(22)

        self.replace_btn = QPushButton("Rep")
        self.replace_btn.setFixedHeight(20)
        self.replace_btn.setFixedWidth(35)
        self.replace_btn.setToolTip("Replace")

        self.replace_all_btn = QPushButton("All")
        self.replace_all_btn.setFixedHeight(20)
        self.replace_all_btn.setFixedWidth(30)
        self.replace_all_btn.setToolTip("Replace All")

        replace_layout.addWidget(self.replace_input)
        replace_layout.addWidget(self.replace_btn)
        replace_layout.addWidget(self.replace_all_btn)

        # Options section - more compact
        options_layout = QHBoxLayout()
        options_layout.setSpacing(10)

        self.case_sensitive = QCheckBox("Aa")
        self.case_sensitive.setToolTip("Match Case")
        self.case_sensitive.setFixedSize(40, 18)

        self.whole_word = QCheckBox("Ab")
        self.whole_word.setToolTip("Match Whole Word")
        self.whole_word.setFixedSize(40, 18)

        self.regex = QCheckBox(".*")
        self.regex.setToolTip("Use Regular Expression")
        self.regex.setFixedSize(40, 18)

        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_word)
        options_layout.addWidget(self.regex)
        options_layout.addStretch()

        # Results label - smaller
        self.results_label = QLabel("No results")
        self.results_label.setStyleSheet("color: #6e6e6e; font-size: 10px;")
        self.results_label.setFixedHeight(14)

        # Close button - smaller
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedHeight(20)

        # Add to main layout
        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addLayout(options_layout)
        layout.addWidget(self.results_label)
        layout.addStretch()
        layout.addWidget(self.close_btn)

        # Connect signals
        self.connect_signals()
        self.update_button_states()

    def connect_signals(self):
        self.find_input.textChanged.connect(self.on_find_text_changed)
        self.find_prev_btn.clicked.connect(self.on_find_prev)
        self.find_next_btn.clicked.connect(self.on_find_next)
        self.replace_btn.clicked.connect(self.on_replace)
        self.replace_all_btn.clicked.connect(self.on_replace_all)
        self.close_btn.clicked.connect(self.hide)

        self.find_input.returnPressed.connect(self.on_find_next)
        self.replace_input.returnPressed.connect(self.on_replace)

    def on_find_text_changed(self, text):
        self.update_button_states()
        if text:
            self.find_next()
        else:
            self.results_label.setText("No results")

    def update_button_states(self):
        has_text = bool(self.find_input.text())
        self.find_prev_btn.setEnabled(has_text)
        self.find_next_btn.setEnabled(has_text)
        self.replace_btn.setEnabled(has_text)
        self.replace_all_btn.setEnabled(has_text)

    def on_find_prev(self):
        self.find_next(forward=False)

    def on_find_next(self):
        self.find_next(forward=True)

    def find_next(self, forward=True):
        text = self.find_input.text()
        if not text:
            return

        options = {
            'case_sensitive': self.case_sensitive.isChecked(),
            'whole_word': self.whole_word.isChecked(),
            'regex': self.regex.isChecked()
        }

        print(f"Finding '{text}' - Direction: {'forward' if forward else 'backward'}, Options: {options}")
        self.results_label.setText("17 results")

    def on_replace(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if find_text:
            print(f"Replacing: '{find_text}' with '{replace_text}'")

    def on_replace_all(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if find_text:
            print(f"Replacing all: '{find_text}' with '{replace_text}'")

    def show_search(self):
        self.show()
        self.find_input.setFocus()
        self.find_input.selectAll()