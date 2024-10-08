import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from ui.main_window import MainWindow
from clipboard_manager import ClipboardManager
from settings_manager import SettingsManager
import keyboard
from PySide6.QtCore import QSettings
from autostart_utils import toggle_autostart
from PySide6.QtGui import QIcon
from ui.system_tray import SystemTray
from ui.suggestion_dialog import SuggestionDialog
import ast

clipboard_manager = None
current_word = ""

def on_key_event(e):
    global current_word
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "space" or e.name == "enter":
            if current_word:
                clipboard_manager.check_and_suggest_word(current_word)
                current_word = ""
        elif e.name == "backspace":
            current_word = current_word[:-1]
        elif len(e.name) == 1:  # אם זה תו בודד
            current_word += e.name

def show_suggestion_dialog(original_text, suggestions):
    print(f"Showing suggestion dialog for: {original_text}")
    print(f"Suggestions: {suggestions}")
    dialog = SuggestionDialog(original_text, ast.literal_eval(suggestions))
    if dialog.exec_():
        final_text = dialog.get_selected_text()
        print(f"User accepted suggestions. Final text: {final_text}")
        keyboard.write(final_text)
    else:
        print("User rejected suggestions")

def main():
    global clipboard_manager
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    settings = QSettings("YourCompany", "KeyboardFixer")
    settings_manager = SettingsManager(settings)
    clipboard_manager = ClipboardManager("ltr")
    clipboard_manager.suggestion_needed.connect(show_suggestion_dialog)
    
    # הוספת מעקב אחר הקלדות
    keyboard.hook(on_key_event)
    
    main_window = MainWindow(clipboard_manager, settings_manager)
    
    system_tray = SystemTray(main_window, clipboard_manager, settings_manager)
    
    # Set up autostart
    autostart = settings.value("autostart", False, type=bool)
    toggle_autostart(autostart)
    
    system_tray.show()
    
    # יצירת אייקון למגש המערכת
    icon = QIcon("resources/icon128.ico")
    tray = QSystemTrayIcon(icon, app)
    
    # יצירת תפריט למגש המערכת
    menu = QMenu()
    exit_action = menu.addAction("יציאה")
    exit_action.triggered.connect(app.quit)
    
    tray.setContextMenu(menu)
    tray.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()