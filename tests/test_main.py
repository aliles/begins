import unittest

import main

class TestMain(unittest.TestCase):

    def test_main_false(self):
        # main.execute() return false outside __main__
        self.assertFalse(main.execute())

if __name__ == '__main__':
    unittest.main()
