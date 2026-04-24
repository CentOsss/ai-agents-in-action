import unittest
from joke_crew import run_joke_crew

class TestJokeCrew(unittest.TestCase):
    def test_basic_functionality(self):
        """Тест базовой функциональности команды шутников"""
        result = run_joke_crew("AI engineer jokes")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_multiple_languages(self):
        """Тест перевода на несколько языков"""
        languages = ["Spanish", "French", "German", "Italian"]
        result = run_joke_crew("AI engineer jokes", languages)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_error_handling(self):
        """Тест обработки ошибок"""
        # Тест с некорректной темой
        result = run_joke_crew("")
        self.assertIsNone(result)

        # Тест с пустым списком языков
        result = run_joke_crew("AI engineer jokes", [])
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main() 