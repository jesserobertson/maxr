""" file: test_parameters.py
"""

import unittest

class TestParameters(unittest.TestCase):

    """ Check that parameters get updated ok
    """

    def setup(self):
        self.p = Parameters()

    def test_setting(self):
        "Equivalent parameters should be updated at the same time"
        for p1, p2 in self.p.equivalent:
            self.p[p1] = 1
            self.assertEqual(1, self.p[p2])

    def test_defaults(self):
        "Defaults should remain set when not set already"
        for par, val in self.p.default_parameters.items():
            self.assertEqual(self.p[par], val)

    def test_attributes(self):
        "Attributes should be copied to the dictionary"
        for par, val in self.p.items():
            self.assertEqual(getattr(self, par), val)

if __name__ == '__main__':
    unittest.main()