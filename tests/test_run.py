import unittest

import begin


class TestExecute(unittest.TestCase):

    def test_execute_false(self):
        # begin.execute() return false outside __main__
        self.assertFalse(begin.execute())

if __name__ == '__main__':
    unittest.begin()
