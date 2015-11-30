import unittest

from name_resolution import is_parent_company

class TestCase(unittest.TestCase):
    def test_is_parent_company(self):
        self.assertTrue(is_parent_company("Exxon Corp", "Exxon Corp DE"))

    def test_is_not_parent_company(self):
        self.assertFalse(is_parent_company("Coca Cola", "Coca Cola Bottling Company Inc"))

    def test_mcdonalds(self):
        self.assertTrue(is_parent_company("MCDONALD'S CORP", "MCDONALDS CORP"))

    def test_apc(self):
        self.assertTrue(is_parent_company("AIR PRODUCTS AND CHEMICALS INC", "AIR PRODUCTS CHEMICALS INC DE"))

    def test_wells_fargo(self):
        self.assertTrue(is_parent_company("WELLS FARGO COMPANY", "WELLS FARGO COMPANY MN"))

    def test_is_parent_company_exact_match(self):
        self.assertTrue(is_parent_company("ARCHER DANIELS MIDLAND", "ARCHER DANIELS MIDLAND"))

    def test_adm_co(self):
        self.assertTrue(is_parent_company("ARCHER DANIELS MIDLAND", "ARCHER DANIELS MIDLAND CO"))