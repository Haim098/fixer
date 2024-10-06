from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, clipboard_manager, settings_manager):
        super().__init__()
        self.clipboard_manager = clipboard_manager
        self.settings_manager = settings_manager
        # ... (שאר הקוד)