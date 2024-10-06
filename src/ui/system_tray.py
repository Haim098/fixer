from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal, QSettings, Slot
import os
from autostart_utils import toggle_autostart

class SystemTray(QSystemTrayIcon):
    def __init__(self, main_window, clipboard_manager, settings_manager):
        super().__init__()
        self.main_window = main_window
        self.clipboard_manager = clipboard_manager
        self.settings_manager = settings_manager
        
        self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "resources", "icon128.png")))
        self.setVisible(True)
        
        self.menu = QMenu()
        self.setup_menu()
        self.setContextMenu(self.menu)
        
    def setup_menu(self):
        show_action = self.menu.addAction("Show")
        show_action.triggered.connect(self.main_window.show)
        
        autostart_action = self.menu.addAction("Run at startup")
        autostart_action.setCheckable(True)
        autostart_action.setChecked(self.settings_manager.settings.value("autostart", False, type=bool))
        autostart_action.triggered.connect(self.toggle_autostart)
        
        quit_action = self.menu.addAction("Quit")
        quit_action.triggered.connect(self.exit_app)
        
    def toggle_autostart(self, state):
        self.settings_manager.settings.setValue("autostart", state)
        toggle_autostart(state)
        
    @Slot()
    def exit_app(self):
        # Implement clean-up logic here if needed
        QApplication.quit()

    def show_message(self, title, message):
        self.showMessage(title, message, QSystemTrayIcon.Information, 3000)