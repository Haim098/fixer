import unittest
from src.converter.engine import convert_text_accurate
from langdetect import detect

class TestConverter(unittest.TestCase):
    def test_eng_to_heb(self):
        self.assertEqual(convert_text_accurate("akuo", "ltr"), "שלום")
        self.assertEqual(convert_text_accurate("cuer", "ltr"), "בוקר")

    def test_heb_to_eng(self):
        self.assertEqual(convert_text_accurate("םמגך", "rtl"), "hello")
        self.assertEqual(convert_text_accurate("ךילה", "rtl"), "night")

    def test_mixed_text(self):
        self.assertEqual(convert_text_accurate("akuo world", "ltr"), "שלום world")
        self.assertEqual(convert_text_accurate("שלום world", "rtl"), "akuo world")

    def test_language_detection(self):
        self.assertEqual(detect("Hello world"), "en")
        self.assertEqual(detect("שלום עולם"), "he")

if __name__ == '__main__':
    unittest.main()