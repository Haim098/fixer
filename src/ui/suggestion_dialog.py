import logging
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut  # Move QShortcut import here

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
        self.setup_shortcuts()

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
        
        self.accept_all_button = QPushButton("קבל הכל (Ctrl+A)")
        self.accept_all_button.clicked.connect(self.accept_all_corrections)
        button_layout.addWidget(self.accept_all_button)

        self.accept_button = QPushButton("קבל נבחרים (Enter)")
        self.accept_button.clicked.connect(self.accept)
        button_layout.addWidget(self.accept_button)

        self.ignore_button = QPushButton("התעלם (Esc)")
        self.ignore_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ignore_button)

        # הוספת תווית להסבר על קיצורי המקלדת החדשים
        shortcut_label = QLabel("השתמש בחצים למעלה/למטה כדי לנווט. חץ למטה מסמן, חץ למעלה מבטל סימון.")
        self.layout.addWidget(shortcut_label)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+A"), self, self.accept_all_corrections)
        QShortcut(QKeySequence("Return"), self, self.accept)
        QShortcut(QKeySequence("Esc"), self, self.reject)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.select_next_item()
        elif event.key() == Qt.Key_Up:
            self.select_previous_item()
        else:
            super().keyPressEvent(event)

    def select_next_item(self):
        current_row = self.list_widget.currentRow()
        next_row = current_row + 1
        if next_row < self.list_widget.count():
            next_item = self.list_widget.item(next_row)
            self.list_widget.setCurrentItem(next_item)
            next_item.setSelected(True)
            logging.info(f"Selected next item: {next_item.text()}")

    def select_previous_item(self):
        current_row = self.list_widget.currentRow()
        prev_row = current_row - 1
        if prev_row >= 0:
            prev_item = self.list_widget.item(prev_row)
            self.list_widget.setCurrentItem(prev_item)
            prev_item.setSelected(True)
            logging.info(f"Selected previous item: {prev_item.text()}")

    def toggle_current_selection(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            current_item.setSelected(not current_item.isSelected())
            logging.info(f"Toggled selection for item: {current_item.text()}")

    def accept_all_corrections(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setSelected(True)
        self.apply_suggestions()
        self.accept()

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