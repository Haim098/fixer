import re
import logging
from PySide6.QtCore import QObject, Signal
from language_utils import detect_language_accurately, is_valid_word
from converter.engine import convert_with_punctuation

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ClipboardManager(QObject):
    suggestion_needed = Signal(str, str)
    conversion_done = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.hebrew_words = set()
        self.load_hebrew_words()
        self.word_buffer = []
        self.valid_word_count = 0

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

        is_valid_in_typed_lang = is_valid_word(word, keyboard_lang)
        converted_word = convert_with_punctuation(word, 'rtl' if keyboard_lang == 'en' else 'ltr')
        is_valid_in_other_lang = is_valid_word(converted_word, 'he' if keyboard_lang == 'en' else 'en')

        if is_valid_in_typed_lang:
            self.reset_buffer()
        else:
            self.word_buffer.append((word, converted_word))
            if is_valid_in_other_lang:
                self.valid_word_count += 1

        if self.valid_word_count >= 3:
            self.suggest_corrections()
        elif len(self.word_buffer) >= 10:  # הגבלת גודל הבאפר למניעת צריכת זיכרון מוגזמת
            self.reset_buffer()

    def reset_buffer(self):
        self.word_buffer.clear()
        self.valid_word_count = 0

    def suggest_corrections(self):
        suggestions = {original: [converted] for original, converted in self.word_buffer}
        original_text = ' '.join(word for word, _ in self.word_buffer)
        self.suggestion_needed.emit(original_text, str(suggestions))
        self.reset_buffer()