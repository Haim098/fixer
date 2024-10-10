import re
import logging
from PySide6.QtCore import QObject, Signal
from converter.engine import convert_with_punctuation
from language_utils import detect_language_accurately, is_valid_word
from keyboard_state import KeyboardState

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ClipboardManager(QObject):
    suggestion_needed = Signal(str, str)
    conversion_done = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.hebrew_words = set()
        self.load_hebrew_words()

    def load_hebrew_words(self):
        try:
            with open('resources/hebrew_words.txt', 'r', encoding='utf-8') as file:
                self.hebrew_words = set(word.strip().lower() for word in file if word.strip())
            logging.info(f"Loaded {len(self.hebrew_words)} words into Hebrew dictionary")
            logging.debug(f"Sample of loaded words: {list(self.hebrew_words)[:10]}")
        except Exception as e:
            logging.error(f"Error loading Hebrew words: {e}")

    def check_and_suggest_word(self, word, context="", keyboard_lang=None):
        logging.info(f"Checking word: '{word}', Context: '{context}', Keyboard language: {keyboard_lang}")
        if not word or not re.search(r'[a-zA-Z\u0590-\u05FF]', word):
            logging.warning("No word to check or no relevant characters")
            return

        detected_lang = detect_language_accurately(word)
        logging.info(f"Detected language: {detected_lang}")

        suggestions = {}

        if keyboard_lang == 'en':
            converted_word = convert_with_punctuation(word, 'rtl')
            if is_valid_word(converted_word, 'he'):
                suggestions[word] = [converted_word]
                logging.info(f"Suggestion found: '{word}' -> '{converted_word}' (Hebrew)")
        elif keyboard_lang == 'he':
            converted_word = convert_with_punctuation(word, 'ltr')
            if is_valid_word(converted_word, 'en'):
                suggestions[word] = [converted_word]
                logging.info(f"Suggestion found: '{word}' -> '{converted_word}' (English)")

        if suggestions:
            logging.info(f"Suggestions: {suggestions}")
            self.suggestion_needed.emit(word, str(suggestions))
        else:
            logging.info(f"No suggestions found for word: '{word}'")