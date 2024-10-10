import logging

# הוסף בתחילת הקובץ
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from langdetect import detect

def convert_text(text, direction):
    print(f"Converting text: {text}, direction: {direction}")  # הדפסת דיבאג
    hebrew_to_english = str.maketrans("אבגדהוזחטיכלמנסעפצקרשתםןץףך", "abgdhvzhtyklmnspzqrstmnzfpk")
    english_to_hebrew = {v: k for k, v in hebrew_to_english.items()}

    if direction == "rtl":
        # המרה מאנגלית לעברית
        return ''.join(english_to_hebrew.get(c, c) for c in text)
    else:
        # המרה מעברית לאנגלית
        return text.translate(hebrew_to_english)

def detect_language(text):
    return detect(text)

# מיפוי מדויק יותר
QWERTY_TO_HEBREW = {
    'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ'
}

HEBREW_TO_QWERTY = {v: k for k, v in QWERTY_TO_HEBREW.items()}

def convert_word(word, direction):
    logging.debug(f"Converting word: '{word}', direction: {direction}")
    result = ''
    for c in word:
        if direction == 'rtl':
            converted = QWERTY_TO_HEBREW.get(c.lower(), c)
            logging.debug(f"RTL: '{c}' -> '{converted}'")
        else:
            converted = HEBREW_TO_QWERTY.get(c, c)
            logging.debug(f"LTR: '{c}' -> '{converted}'")
        result += converted
    logging.debug(f"Conversion result for '{word}': '{result}'")
    return result

def convert_text_accurate(text, direction):
    logging.info(f"Converting text: '{text}', direction: {direction}")
    words = text.split()
    converted_words = []
    for word in words:
        converted_word = convert_word(word, direction)
        logging.debug(f"Word: '{word}', Converted: '{converted_word}'")
        converted_words.append(converted_word)
    result = ' '.join(converted_words)
    logging.info(f"Conversion result: '{result}'")
    return result

# טיפול בסימני פיסוק
PUNCTUATION = {',': 'ת', '.': 'ץ', '/': 'ק', "'": 'ר', '-': 'ף'}

def convert_with_punctuation(text, direction):
    logging.debug(f"Converting text with punctuation: '{text}', direction: {direction}")
    words = text.split()
    converted_words = []
    for word in words:
        converted_word = ''
        for char in word:
            if direction == 'rtl':
                converted_char = QWERTY_TO_HEBREW.get(char.lower(), PUNCTUATION.get(char, char))
            else:
                converted_char = HEBREW_TO_QWERTY.get(char, {v: k for k, v in PUNCTUATION.items()}.get(char, char))
            converted_word += converted_char
        converted_words.append(converted_word)
        logging.debug(f"Converted word: '{word}' -> '{converted_word}'")
    result = ' '.join(converted_words)
    logging.debug(f"Final conversion result: '{result}'")
    return result

# הוסף פונקציית בדיקה
def test_conversion():
    test_cases = [
        ("akuo", "שלום"),
        ("שלום", "akuo"),
        ("hello", "יקךךם"),
        ("עברית", "gcrh,"),
        ("יקךךם", "hello"),
        ("tnt", "אמא"),
        ("mother", "צםאיקר"),
    ]
    for input_text, expected_output in test_cases:
        direction = 'rtl' if any("\u0590" <= char <= "\u05FF" for char in input_text) else 'ltr'
        result = convert_with_punctuation(input_text, direction)
        logging.info(f"Test case - Input: {input_text}, Expected: {expected_output}, Got: {result}")
        assert result == expected_output, f"Conversion failed for {input_text}"

# הפעל את פונקציית הבדיקה אם הקובץ מורץ ישירות
if __name__ == "__main__":
    test_conversion()