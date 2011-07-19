import unittest

import main


class TestExecute(unittest.TestCase):

    def test_execute_false(self):
        # main.execute() return false outside __main__
        self.assertFalse(main.execute())

if __name__ == '__main__':
    unittest.main()
