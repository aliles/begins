import unittest

import begin


class TestStart(unittest.TestCase):

    def test_start_false(self):
        # begin.start() return false outside __main__
        self.assertFalse(begin.start())

if __name__ == '__main__':
    unittest.begin()
