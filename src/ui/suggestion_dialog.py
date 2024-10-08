from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem

class SuggestionDialog(QDialog):
    def __init__(self, original_text, suggestions):
        super().__init__()
        self.setWindowTitle("הצעות תיקון")
        self.layout = QVBoxLayout()
        self.original_text = original_text
        self.suggestions = suggestions
        self.selected_text = original_text

        print(f"SuggestionDialog initialized with text: {original_text}")
        print(f"Suggestions: {suggestions}")

        self.label = QLabel(f"הטקסט המקורי: {original_text}")
        self.layout.addWidget(self.label)

        self.list_widget = QListWidget()
        for word, candidates in suggestions.items():
            item = QListWidgetItem(f"{word} -> {candidates[0]}")
            item.setData(100, word)
            item.setData(101, candidates[0])
            self.list_widget.addItem(item)
        self.list_widget.itemDoubleClicked.connect(self.apply_suggestion)
        self.layout.addWidget(self.list_widget)

        self.accept_button = QPushButton("קבל תיקונים")
        self.accept_button.clicked.connect(self.accept)
        self.layout.addWidget(self.accept_button)

        self.setLayout(self.layout)

    def apply_suggestion(self, item):
        word = item.data(100)
        suggestion = item.data(101)
        self.selected_text = self.selected_text.replace(word, suggestion)
        print(f"Applied suggestion: {word} -> {suggestion}")

    def get_selected_text(self):
        return self.selected_text

    def accept(self):
        print(f"User accepted changes. Final text: {self.selected_text}")
        super().accept()