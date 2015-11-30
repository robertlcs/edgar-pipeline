import unittest

from cleaning import strip_issuer_name

class CleaningTests(unittest.TestCase):
    #def __init__(self):
    #    self.issuers_to_clean = {'WHIRLPOOL CORP DE' : 'WHIRLPOOL',
    #                             'WESTERN UNION CO' : 'WESTERN UNION'
     #                     }

    def test_strip_issuer(self):
        self.issuers_to_clean = {'WHIRLPOOL CORP DE' : 'WHIRLPOOL',
                                 'WESTERN UNION CO' : 'WESTERN UNION'
                          }
        for company in self.issuers_to_clean.keys():
            self.assertEqual(self.issuers_to_clean[company], strip_issuer_name(company))

