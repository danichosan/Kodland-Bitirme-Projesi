import unittest
from AI.ai_engine import get_career_suggestions

class TestAISuggestions(unittest.TestCase):
    def test_keyword_matching(self):
        input_text = "programlama ve yazılım"
        results = get_career_suggestions(input_text)
        self.assertIn("Yazılım Mühendisi", results)

if __name__ == '__main__':
    unittest.main()