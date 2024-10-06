import unittest
from src.converter.engine import convert_text

class TestConverter(unittest.TestCase):
    def test_eng_to_heb(self):
        self.assertEqual(convert_text("akuo", "eng_to_heb"), "שלום")
        self.assertEqual(convert_text("cuer", "eng_to_heb"), "בוקר")

    def test_heb_to_eng(self):
        self.assertEqual(convert_text("םמגך", "heb_to_eng"), "hello")
        self.assertEqual(convert_text("ךילה", "heb_to_eng"), "night")

    def test_mixed_text(self):
        self.assertEqual(convert_text("akuo world", "eng_to_heb"), "שלום דםרלג")
        self.assertEqual(convert_text("שלום world", "heb_to_eng"), "akuo world")

if __name__ == '__main__':
    unittest.main()