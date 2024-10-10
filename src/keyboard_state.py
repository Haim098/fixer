import ctypes
import logging

# הגדרת הלוגר
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# קודים של שפות מקלדת
HEBREW_KEYBOARD = 0x40D
ENGLISH_KEYBOARD = 0x409

class KeyboardState:
    @staticmethod
    def get_keyboard_language():
        """
        מחזיר את שפת המקלדת הנוכחית (עברית או אנגלית)
        """
        user32 = ctypes.windll.user32
        current_window = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(current_window, 0)
        keyboard_layout = user32.GetKeyboardLayout(thread_id)
        language_id = keyboard_layout & 0xFFFF

        if language_id == HEBREW_KEYBOARD:
            logging.debug("Current keyboard language: Hebrew")
            return 'he'
        elif language_id == ENGLISH_KEYBOARD:
            logging.debug("Current keyboard language: English")
            return 'en'
        else:
            logging.warning(f"Unknown keyboard language ID: {language_id}")
            return 'unknown'

    @staticmethod
    def is_caps_lock_on():
        """
        בודק אם Caps Lock מופעל
        """
        caps_lock_state = ctypes.windll.user32.GetKeyState(0x14)
        is_on = caps_lock_state != 0
        logging.debug(f"Caps Lock is {'on' if is_on else 'off'}")
        return is_on

    @staticmethod
    def switch_keyboard_language():
        """
        מחליף את שפת המקלדת בין עברית לאנגלית
        """
        user32 = ctypes.windll.user32
        user32.keybd_event(0x15, 0, 0, 0)  # Press the key
        user32.keybd_event(0x15, 0, 2, 0)  # Release the key
        logging.info("Keyboard language switched")

# בדיקה של הפונקציות
if __name__ == "__main__":
    print("Current keyboard language:", KeyboardState.get_keyboard_language())
    print("Is Caps Lock on?", KeyboardState.is_caps_lock_on())
    print("Switching keyboard language...")
    KeyboardState.switch_keyboard_language()
    print("Current keyboard language after switch:", KeyboardState.get_keyboard_language())