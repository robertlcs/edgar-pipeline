import unittest

from geocoding.address import parse, clean

class AddressTests(unittest.TestCase):

    def setUp(self):
        with open("geocoding/mnt_view_addr.json", "r") as f:
            self.fake_addr1 = f.read()
        with open("geocoding/3m_addr.json", "r") as f:
            self.fake_addr2 = f.read()

    def test_parse_response(self):
        (street1, city, state, postal, country) = parse(self.fake_addr1)
        self.assertEqual('1600 Amphitheatre Pkwy', street1)
        self.assertEqual('Mountain View', city)
        self.assertEqual('California', state)
        self.assertEqual('94043', postal)
        self.assertEqual('United States', country)

    def test_parse_response2(self):
        (street1, city, state, postal, country) = parse(self.fake_addr2)
        self.assertEqual("14th Street", street1)
        self.assertEqual("Saint Paul", city)
        self.assertEqual('Minnesota', state)
        self.assertEqual('55144', postal)
        self.assertEqual('United States', country)

    @unittest.skip("Don't call this -- it's expensive")
    def test_clean_weird_chinese_address(self):
        addr = clean('M5 1 Jiuxianqiao East Road, Chaoyang District, Beijing 100016, People s Republic of China')
        self.assertEqual(None, addr)

    def test_zero_results(self):
        zero_results = '''{
   "results" : [],
   "status" : "ZERO_RESULTS"
}
'''
        self.assertEqual(None, parse(zero_results))

    def test_clean_ireland_address(self):
        addr = clean("70 SIR JOHN ROGERSON'S QUAY, Dublin 2, L2 2, Ireland")
        self.assertEqual((u"70 Sir John Rogerson's Quay", u'Dublin', u'Dublin', None, u'Ireland'), addr)




