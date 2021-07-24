import unittest
from functions import *

# Tests for functions.py
class TestGetClanmateNames(unittest.TestCase):
    # Warning: this test only checks that some names are returned, and that those contain a few known ones, doesn't check that
    # all the names are returned because of the fluid nature of clan membership
    def test_get_clanmate_names(self):
        res = get_clanmate_names('Acorn')

        # Checking against Acorn with players who don't change their rsn's
        self.assertIn('Mrawr', res)
        self.assertIn('Gadnuka', res)
        self.assertIn('CompCake', res)
        self.assertIn('MiracleEdrea', res)

class TestGetCurrentXpAll(unittest.TestCase):
    def test_get_current_xp_all(self):
        res = get_current_xp_all(['Andy Hunts', 'Mrawr', 'Gadnuka', 'CompCake'])

        self.assertEqual(res[0][0], 'Andy Hunts')
        self.assertEqual(res[2][0], 'Gadnuka')
        self.assertEqual(res[3][0], 'CompCake')
        # Current xp is always changing, with the exception of players with 200m in a skill, so test against known 200ms
        resMrawr = res[1]
        self.assertEqual(resMrawr[0], 'Mrawr')
        self.assertEqual(resMrawr[INVENTION], 200000000)
        self.assertEqual(resMrawr[HUNTER], 200000000)
        self.assertEqual(resMrawr[MAGIC], 200000000)
        self.assertEqual(resMrawr[DEFENCE], 200000000)

class TestStoreXpInFile(unittest.TestCase):
    def test_store_xp_in_file(self):
        pass

class TestPullXpFromFile(unittest.TestCase):
    def test_pull_xp_from_file(self):
        pass

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

class TestFilterNoXpGained(unittest.TestCase):
    def test_one_with_none(self):
        res = filter_no_xp_gained([['CompCake', 0]])
        self.assertEqual(res, [])

    def test_one_with_xp(self):
        res = filter_no_xp_gained([['Andy Hunts', 780334]])
        self.assertEqual(res, [['Andy Hunts', 780334]])

    def test_mult_with_one_none(self):
        res = filter_no_xp_gained([['Andy Hunts', 780334], ['Gadnuka', 93022], ['CompCake', 0]])
        self.assertEqual(res, [['Andy Hunts', 780334], ['Gadnuka', 93022]])

    def test_mult_with_none_none(self):
        res = filter_no_xp_gained([['Andy Hunts', 780334], ['Gadnuka', 93022], ['CompCake', 900]])
        self.assertEqual(res, [['Andy Hunts', 780334], ['Gadnuka', 93022], ['CompCake', 900]])

# Tests for run_cmd.py

if __name__ == '__main__':
    unittest.main()
