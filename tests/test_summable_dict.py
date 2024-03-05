from unittest import TestCase

from ledboardclientfull.python_extensions.summable_dict import SummableDict


class TestSummableDict(TestCase):

    def setUp(self):
        self.a = SummableDict()
        self.a[0] = [1, 2, 3]
        self.a[1] = 1

        self.b = SummableDict()
        self.b[0] = [4, 5, 6]
        self.b[1] = 2

        self.s = SummableDict()
        self.s[0] = [1, 2, 3, 4, 5, 6]
        self.s[1] = 3

        self.s_sym = SummableDict()
        self.s_sym[0] = [4, 5, 6, 1, 2, 3]
        self.s_sym[1] = 3

    def test_sum(self):
        self.assertEqual(
            self.a + self.b,
            self.s
        )

    def test_sum_symmetry(self):
        self.assertEqual(
            self.b + self.a,
            self.s_sym
        )

    def test_sum_with_empty(self):
        self.assertEqual(
            self.a + SummableDict(),
            self.a
        )
