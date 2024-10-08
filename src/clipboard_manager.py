import re
from langdetect import detect
from PySide6.QtCore import QObject, Signal
import pyperclip
from converter.engine import convert_text_accurate
from spellchecker import SpellChecker

class ClipboardManager(QObject):
    suggestion_needed = Signal(str, str)
    conversion_done = Signal(str, str)

    def __init__(self, default_direction):
        super().__init__()
        self.default_direction = default_direction
        self.last_value = ""
        self.spell_checker_en = SpellChecker(language='en')
        self.hebrew_words = set()
        self.load_hebrew_words()

    def detect_language(self, text):
        if re.search(r'[\u0590-\u05FF]', text):
            return 'he'
        elif re.search(r'[a-zA-Z]', text):
            return 'en'
        return detect(text)

    def load_hebrew_words(self):
        try:
            with open('resources/hebrew_words.txt', 'r', encoding='utf-8') as file:
                self.hebrew_words = set(word.strip() for word in file if word.strip())
            print(f"Loaded {len(self.hebrew_words)} words into Hebrew dictionary")
        except Exception as e:
            print(f"Error loading Hebrew words: {e}")

    def start_monitoring(self):
        pass

    def check_clipboard(self):
        tmp_value = pyperclip.paste()
        if tmp_value != self.last_value:
            self.last_value = tmp_value
            self.on_clipboard_change()

    def on_clipboard_change(self):
        print(f"Clipboard changed: {self.last_value}")
        self.check_and_suggest()

    def set_direction(self, direction):
        self.default_direction = direction

    def convert_and_paste(self):
        text = pyperclip.paste()
        if text:
            detected_lang = self.detect_language(text)
            direction = 'rtl' if detected_lang == 'he' else 'ltr'
            converted = convert_text_accurate(text, direction)
            pyperclip.copy(converted)
            self.conversion_done.emit("המרה הושלמה", f"הטקסט הומר בהצלחה: {converted[:20]}...")

    def check_and_suggest(self):
        text = self.last_value
        print(f"Checking text: {text}")
        if not text or not re.search(r'[a-zA-Z\u0590-\u05FF]', text):
            print("No text to check or no relevant characters")
            return

        detected_lang = self.detect_language(text)
        print(f"Detected language: {detected_lang}")

        words = re.findall(r'\b[a-zA-Z\u0590-\u05FF]+\b', text)
        suggestions = {}

        for word in words:
            if detected_lang == 'he':
                if word not in self.hebrew_words and word not in self.spell_checker_he.word_frequency:
                    converted = convert_text_accurate(word, 'ltr')
                    if converted.lower() in self.spell_checker_en.word_frequency:
                        suggestions[word] = [converted]
            else:
                if word.lower() not in self.spell_checker_en.word_frequency:
                    converted = convert_text_accurate(word, 'rtl')
                    if converted in self.hebrew_words or converted in self.spell_checker_he.word_frequency:
                        suggestions[word] = [converted]

        if suggestions:
            print(f"Suggestions: {suggestions}")
            self.suggestion_needed.emit(text, str(suggestions))
        else:
            print("No suggestions found")
            self.conversion_done.emit("בדיקה הושלמה", "לא נמצאו הצעות לתיקון")

    def check_and_suggest_word(self, word):
        print(f"Checking word: {word}")
        if not word or not re.search(r'[a-zA-Z\u0590-\u05FF]', word):
            print("No word to check or no relevant characters")
            return

        detected_lang = self.detect_language(word)
        print(f"Detected language: {detected_lang}")

        suggestions = {}

        if detected_lang == 'en':
            # Logic for English input
            if word.lower() in self.spell_checker_en.word_frequency:
                print("Word is valid in English, no suggestion needed")
            else:
                # Convert to Hebrew (as if typed on Hebrew keyboard)
                converted = convert_text_accurate(word, 'rtl')
                if converted in self.hebrew_words:
                    suggestions[word] = [converted]
                else:
                    print("Converted word not found in Hebrew dictionary, no suggestion")

        elif detected_lang == 'he':
            # Logic for Hebrew input
            if word in self.hebrew_words:
                print("Word is valid in Hebrew, no suggestion needed")
            else:
                # Convert to English (as if typed on English keyboard)
                converted = convert_text_accurate(word, 'ltr')
                if converted.lower() in self.spell_checker_en.word_frequency:
                    suggestions[word] = [converted]
                else:
                    print("Converted word not found in English dictionary, no suggestion")

        if suggestions:
            print(f"Suggestions: {suggestions}")
            self.suggestion_needed.emit(word, str(suggestions))
        else:
            print(f"No suggestions found for word: {word}")

    def is_hebrew_typed_in_english(self, word):
        hebrew_chars = 'אבגדהוזחטיכלמנסעפצקרשת'
        english_chars = 'tcsduvzjyhfknbxgpmera,'
        trans_table = str.maketrans(english_chars, hebrew_chars)
        converted = word.translate(trans_table)
        return converted if converted in self.hebrew_words else None