import unittest
from io import StringIO
from AWScre import AWScre

class TestAWSCre(unittest.TestCase):
    
    def setUp(self):
        self.a = AWScre("credentialsfile","out.yml","example-account")

    def test_validate(self):
        exampleline = "wibble_goat = 123"
        self.assertTrue(self.a.ValidateLine(exampleline))
        badline = "# I ❤️ kippers"
        self.assertFalse(self.a.ValidateLine(badline))

    def test_ConvertLine(self):
        given = "wibble = frank\n"
        wants = "  WIBBLE: frank\n"
        self.assertEqual(self.a.ConvertLine(given), wants)

    def test_LoadLines(self):
            example = StringIO("[dud-account]\nmarcus = garvey\n[example-account]\nkey1 = abc\nkey2 = def\nkey3 = ghi\n\ngarbage\n")
            given = self.a.LoadLines(example)
            self.assertEqual(len(given), 3)
            wanted1 = "  KEY1: abc\n"
            self.assertEqual(given[0], wanted1)
            example2 = StringIO("[dud-account]\nmarcus = garvey\n[example-account]\nkey1 = fruitcage\nkey2 = def\nkey3 = ghi\n")
            given = self.a.LoadLines(example2)
            wanted2 = "  KEY1: fruitcage\n"
            self.assertEqual(given[0], wanted2)
if __name__ == '__main__':
    unittest.main()