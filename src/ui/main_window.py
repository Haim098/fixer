from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QTextCursor

class MainWindow(QMainWindow):
    def __init__(self, clipboard_manager, settings_manager):
        super().__init__()
        self.clipboard_manager = clipboard_manager
        self.settings_manager = settings_manager
        self.setWindowTitle("KeyboardFixer")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

    # הסרנו את המתודה on_text_changed שגרמה לשגיאות