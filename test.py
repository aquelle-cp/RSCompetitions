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

class TestCalcCompGains(unittest.TestCase):
    def test_one_skill(self):
        gains = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        skills = [ATTACK]

        res = calc_comp_gains(gains, skills)

        expected = [['test1', 30], ['test2', 43], ['test3', 32], ['test4', 40]]

    def test_two_skills(self):
        gains = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        skills = [ATTACK, DEFENCE]

        res = calc_comp_gains(gains, skills)

        expected = [['test1', 54], ['test2', 44], ['test3', 44], ['test4', 51]]

    def test_three_skills(self):
        gains = [['test1', 90, 30, 24], ['test2', 11, 43, 1], ['test3', 48, 32, 12], ['test4', 120, 40, 11]]
        skills = [OVERALL, ATTACK, DEFENCE]

        res = calc_comp_gains(gains, skills)

        expected = [['test1', 144], ['test2', 55], ['test3', 92], ['test4', 171]]

if __name__ == '__main__':
    unittest.main()
