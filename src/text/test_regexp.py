from unittest import TestCase
import re


class TestRegexp(TestCase):
    def test_match(self):
        pattern = '^\(?0\d{2}[\)\-\s]?\d{8}$|^\(?0\d{3}[\)\-\s]?\d{7}$|^1\d{10}$'

        self.assertTrue(re.match(pattern, '(029)85556666'))
        self.assertTrue(re.match(pattern, '029-85556666'))
        self.assertTrue(re.match(pattern, '029 85556666'))
        self.assertTrue(re.match(pattern, '(0917)8556666'))
        self.assertTrue(re.match(pattern, '0917-8556666'))
        self.assertTrue(re.match(pattern, '0917 8556666'))
        self.assertTrue(re.match(pattern, '13991300001'))