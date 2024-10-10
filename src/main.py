import sys
import logging
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
from spellchecker import SpellChecker
from keyboard_state import KeyboardState
import pyperclip

# הגדרת הלוגר
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

clipboard_manager = None
current_word = ""

def on_key_event(e):
    global current_word
    if e.event_type == keyboard.KEY_DOWN:
        if e.name in ["space", "enter", ".", ",", "!", "?"]:
            if current_word:
                context = get_surrounding_context(current_word)
                keyboard_lang = KeyboardState.get_keyboard_language()
                clipboard_manager.check_and_suggest_word(current_word, context, keyboard_lang)
                current_word = ""
        elif e.name == "backspace":
            current_word = current_word[:-1]
        elif len(e.name) == 1:
            current_word += e.name

def get_surrounding_context(word):
    # TODO: Implement logic to get surrounding words
    return ""

def show_suggestion_dialog(original_text, suggestions):
    logging.info(f"Showing suggestion dialog for: '{original_text}'")
    logging.debug(f"Suggestions: {suggestions}")
    dialog = SuggestionDialog(original_text, ast.literal_eval(suggestions))
    if dialog.exec():
        final_text = dialog.get_selected_text()
        logging.info(f"User accepted suggestions. Final text: '{final_text}'")
        replace_text(original_text, final_text)
    else:
        logging.info("User rejected suggestions")

def replace_text(original_text, new_text):
    logging.debug(f"Replacing '{original_text}' with '{new_text}'")
    # Delete one extra character before the original text
    keyboard.press_and_release('backspace')
    # Delete the original text
    for _ in range(len(original_text)):
        keyboard.press_and_release('backspace')
    # Type the new text
    keyboard.write(new_text)
    # Add a space after the new text
    keyboard.press_and_release('space')
    # Copy the new text to clipboard
    pyperclip.copy(new_text)
    # Check if the text was actually replaced
    current_text = get_current_text()
    if current_text.strip() != new_text.strip():
        logging.error(f"Text replacement failed. Expected: '{new_text}', Got: '{current_text}'")
    else:
        logging.info("Text replacement successful")

def get_current_text():
    return pyperclip.paste()

def main():
    global clipboard_manager
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    settings = QSettings("YourCompany", "KeyboardFixer")
    settings_manager = SettingsManager(settings)
    clipboard_manager = ClipboardManager()  # הסרנו את הארגומנט "ltr"
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