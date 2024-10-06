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
    print(f"Detecting language for: {text}")  # הדפסת דיבאג
    hebrew_chars = set('אבגדהוזחטיכלמנסעפצקרשתםןץףך')
    english_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    hebrew_count = sum(1 for char in text if char in hebrew_chars)
    english_count = sum(1 for char in text if char in english_chars)
    
    print(f"Hebrew count: {hebrew_count}, English count: {english_count}")  # הדפסת דיבאג
    
    if hebrew_count > english_count:
        return "ltr"  # מעברית לאנגלית
    else:
        return "rtl"  # מאנגלית לעברית

# מיפוי מדויק יותר
QWERTY_TO_HEBREW = {
    'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ'
}

HEBREW_TO_QWERTY = {v: k for k, v in QWERTY_TO_HEBREW.items()}

def convert_text_accurate(text, direction):
    print(f"Converting text: {text}, direction: {direction}")  # הדפסת דיבאג
    if direction == "rtl":
        # המרה מאנגלית לעברית
        return ''.join(QWERTY_TO_HEBREW.get(c.lower(), c) for c in text)
    else:
        # המרה מעברית לאנגלית
        return ''.join(HEBREW_TO_QWERTY.get(c, c) for c in text)

# הוסף פונקציית בדיקה
def test_conversion():
    test_cases = [
        ("akuo", "שלום"),
        ("שלום", "akuo"),
        ("hello", "הללו"),
        ("עברית", "gcrh,"),
    ]
    for input_text, expected_output in test_cases:
        direction = detect_language(input_text)
        result = convert_text_accurate(input_text, direction)
        print(f"Input: {input_text}, Expected: {expected_output}, Got: {result}")

# הפעל את פונקציית הבדיקה אם הקובץ מורץ ישירות
if __name__ == "__main__":
    test_conversion()