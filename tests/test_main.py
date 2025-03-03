import unittest
from src.main import main

class TestMain(unittest.TestCase):
    
    def test_main_function(self):
        # Здесь вы можете добавить тесты для функции main()
        self.assertIsNone(main())  # Пример проверки, что функция возвращает None

if __name__ == '__main__':
    unittest.main()