import logging
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SuggestionDialog(QDialog):
    def __init__(self, original_text, suggestions, context=""):
        super().__init__()
        self.setWindowTitle("הצעות תיקון")
        self.layout = QVBoxLayout()
        self.original_text = original_text
        self.suggestions = suggestions
        self.context = context
        self.selected_text = original_text

        self.setup_ui()

    def setup_ui(self):
        # הצגת ההקשר
        if self.context:
            context_layout = QHBoxLayout()
            context_label = QLabel("הקשר:")
            context_text = QLabel(self.context)
            context_text.setStyleSheet("font-weight: bold;")
            context_layout.addWidget(context_label)
            context_layout.addWidget(context_text)
            self.layout.addLayout(context_layout)

        # הצגת הטקסט המקורי
        original_layout = QHBoxLayout()
        original_label = QLabel("טקסט מקורי:")
        original_text = QLabel(self.original_text)
        original_text.setStyleSheet("font-weight: bold;")
        original_layout.addWidget(original_label)
        original_layout.addWidget(original_text)
        self.layout.addLayout(original_layout)

        # רשימת ההצעות
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        for word, candidates in self.suggestions.items():
            for candidate in candidates:
                item = QListWidgetItem(f"{word} -> {candidate}")
                item.setData(Qt.UserRole, (word, candidate))
                self.list_widget.addItem(item)
        self.layout.addWidget(self.list_widget)

        # כפתורים
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("קבל תיקונים")
        self.accept_button.clicked.connect(self.accept)
        button_layout.addWidget(self.accept_button)

        self.ignore_button = QPushButton("התעלם")
        self.ignore_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ignore_button)

        self.ignore_always_button = QPushButton("התעלם תמיד")
        self.ignore_always_button.clicked.connect(self.ignore_always)
        button_layout.addWidget(self.ignore_always_button)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def apply_suggestions(self):
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            original, suggestion = item.data(Qt.UserRole)
            self.selected_text = self.selected_text.replace(original, suggestion)
        logging.info(f"Applied suggestions. Updated text: {self.selected_text}")

    def get_selected_text(self):
        return self.selected_text

    def accept(self):
        self.apply_suggestions()
        logging.info(f"User accepted changes. Final text: {self.selected_text}")
        super().accept()

    def ignore_always(self):
        # TODO: Implement logic to save words to be always ignored
        logging.info("Ignore always clicked")
        self.reject()