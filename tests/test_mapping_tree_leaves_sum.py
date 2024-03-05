from unittest import TestCase

from ledboardclientfull.core.entities.mapping_tree.leaves import Leaves, LeavesUniverse


class TestSummableDict(TestCase):

    def setUp(self):
        self.a = Leaves()
        self.a.universes[0] = LeavesUniverse(index=0)
        self.a.universes[0].leaves[0]

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
