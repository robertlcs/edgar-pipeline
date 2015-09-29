import unittest

from name_utils import is_parent_company

class TestCase(unittest.TestCase):
    def test_is_parent_company(self):
        self.assertTrue(is_parent_company("Exxon Corp", "Exxon Corp DE"))

    def test_is_not_parent_company(self):
        self.assertFalse(is_parent_company("Coca Cola", "Coca Cola Bottling Company Inc"))

    def test_mcdonalds(self):
        self.assertTrue(is_parent_company("MCDONALD'S CORP", "MCDONALDS CORP"))

    def test_apc(self):
        self.assertTrue(is_parent_company("AIR PRODUCTS AND CHEMICALS INC", "AIR PRODUCTS CHEMICALS INC DE"))