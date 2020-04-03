import unittest
from competitions import *

class TestCalcXPGained(unittest.TestCase):
    def test_same_names(self):
        old = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        new = [['test1', 90, 30, 322], ['test2', 11, 43, 424], ['test3', 48, 32, 4244], ['test4', 120, 40, 111]]

        res = calc_xp_gained(old, new)

        expected = [['test1', 0, 0, 298], ['test2', 0, 0, 423], ['test3', 0, 0, 4232], ['test4', 0, 0, 100]]

        self.assertEqual(res, expected)

    def test_changed_name(self):
        old = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        new = [['test5', 90, 30, 322], ['test2', 11, 43, 424], ['test3', 48, 32, 4244], ['test4', 120, 40, 111]]

        res = calc_xp_gained(old, new)

        expected = [['test2', 0, 0, 423], ['test3', 0, 0, 4232], ['test4', 0, 0, 100]]

        self.assertEqual(res, expected)

    def test_user_went_inactive(self):
        old = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        new = [['test2', 11, 43, 424], ['test3', 48, 32, 4244], ['test4', 120, 40, 111]]

        res = calc_xp_gained(old, new)

        expected = [['test2', 0, 0, 423], ['test3', 0, 0, 4232], ['test4', 0, 0, 100]]

        self.assertEqual(res, expected)

    def test_new_member(self):
        old = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        new = [['test1', 90, 30, 24], ['test2', 11, 43, 424], ['test3', 48, 32, 4244], ['test4', 120, 40, 111], ['test5', 90, 30, 24]]

        res = calc_xp_gained(old, new)

        expected = [['test1', 0, 0, 0], ['test2', 0, 0, 423], ['test3', 0, 0, 4232], ['test4', 0, 0, 100]]

        self.assertEqual(res, expected)

    def test_order_changed(self):
        old = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        new = [['test2', 11, 43, 424], ['test3', 48, 32, 4244], ['test4', 120, 40, 111], ['test1', 90, 30, 322]]

        res = calc_xp_gained(old, new)

        expected = [['test1', 0, 0, 298], ['test2', 0, 0, 423], ['test3', 0, 0, 4232], ['test4', 0, 0, 100]]

        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
