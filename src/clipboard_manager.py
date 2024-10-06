import pyperclip
from PySide6.QtCore import QObject, Signal
from converter.engine import convert_text, detect_language

class HistoryManager(QObject):
    history_updated = Signal(list)

    def __init__(self):
        super().__init__()
        self.history = []

    def add_to_history(self, text):
        self.history.append(text)
        self.history_updated.emit(self.history)

class ClipboardManager(QObject):
    conversion_done = Signal(str, str)

    def __init__(self, default_direction):
        super().__init__()
        self.default_direction = default_direction
        self.history_manager = HistoryManager()

    def start_monitoring(self):
        # לא נדרש כרגע, אבל אפשר להוסיף מנגנון ניטור אם נדרש
        pass  # הוספנו 'pass' כדי שהפונקציה לא תהיה ריקה

    def on_clipboard_change(self):
        text = pyperclip.paste()
        print(f"Clipboard changed: {text}")
        self.history_manager.add_to_history(text)

    def set_direction(self, direction):
        self.default_direction = direction

    def convert_and_paste(self):
        text = pyperclip.paste()
        if text:
            direction = detect_language(text)
            converted = convert_text(text, direction)
            pyperclip.copy(converted)
            self.conversion_done.emit("המרה הושלמה", f"הטקסט הומר בהצלחה: {converted[:20]}...")