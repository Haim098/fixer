import logging
from langdetect import detect
from spellchecker import SpellChecker

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

spell_checker_en = SpellChecker(language='en')
hebrew_words = set()

def detect_language_accurately(text):
    if any("\u0590" <= char <= "\u05FF" for char in text):
        return 'he'
    elif text.isascii() and any(char.isalpha() for char in text):
        return 'en'
    try:
        return detect(text)
    except:
        return 'unknown'

def is_valid_word(word, language):
    word = word.lower()
    if language == 'en':
        return word in spell_checker_en or word in spell_checker_en.word_frequency
    elif language == 'he':
        return word in hebrew_words
    return False

def load_hebrew_words():
    global hebrew_words
    with open('resources/hebrew_words.txt', 'r', encoding='utf-8') as f:
        hebrew_words = set(word.strip().lower() for word in f)
    logging.info(f"Loaded {len(hebrew_words)} Hebrew words")

load_hebrew_words()