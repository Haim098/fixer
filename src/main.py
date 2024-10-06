import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from ui.main_window import MainWindow
from clipboard_manager import ClipboardManager
from settings_manager import SettingsManager
import keyboard
from converter.engine import convert_text_accurate, detect_language
import pyperclip
from PySide6.QtCore import QSettings, QCoreApplication
from autostart_utils import toggle_autostart
import time
from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from ui.system_tray import SystemTray

original_clipboard = ""

def smart_convert_and_paste():
    global original_clipboard
    print("smart_convert_and_paste triggered")
    
    # קבלת הטקסט הנוכחי מהלוח
    text = pyperclip.paste()
    print(f"Text to convert: '{text}'")
    
    if text and text.strip():  # בדיקה שהטקסט לא ריק
        original_clipboard = text
        direction = detect_language(text)
        converted = convert_text_accurate(text, direction)
        print(f"Converted text: '{converted}'")
        
        if converted != text:  # בדיקה שהטקסט אכן השתנה
            pyperclip.copy(converted)
            print("Text converted and copied to clipboard")
            
            # הדבקת הטקסט המומר
            time.sleep(0.1)  # המתנה קצרה לפני ההדבקה
            keyboard.send('ctrl+v')
            print("Converted text pasted")
        else:
            print("Text didn't change after conversion")
    else:
        print("No text to convert or text is empty")

def restore_original_clipboard():
    global original_clipboard
    if original_clipboard:
        pyperclip.copy(original_clipboard)
        print(f"Restored original text to clipboard: '{original_clipboard}'")
    else:
        print("No original text to restore")

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    settings = QSettings("YourCompany", "KeyboardFixer")
    settings_manager = SettingsManager(settings)
    clipboard_manager = ClipboardManager("ltr")
    
    main_window = MainWindow(clipboard_manager, settings_manager)
    
    system_tray = SystemTray(main_window, clipboard_manager, settings_manager)
    
    # Set up autostart
    autostart = settings.value("autostart", False, type=bool)
    toggle_autostart(autostart)
    
    # Set up global hotkeys
    keyboard.add_hotkey('ctrl+shift+v', smart_convert_and_paste, suppress=True)
    keyboard.add_hotkey('ctrl+shift+b', restore_original_clipboard, suppress=True)
    
    system_tray.show()
    
    # Add a global shortcut for quitting the application
    shortcut = QShortcut(QKeySequence("Ctrl+Q"), main_window)
    shortcut.activated.connect(system_tray.exit_app)

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