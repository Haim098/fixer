from PySide6.QtCore import QSettings

class SettingsManager:
    def __init__(self, settings=None):
        if settings is None:
            self.settings = QSettings("YourCompany", "KeyboardFixer")
        else:
            self.settings = settings