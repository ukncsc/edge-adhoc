import unittest
from adapters.certuk_adhoc.views.queries import generate_matches_array, plain_text_response

class QueryResponseTests(unittest.TestCase):

    address_id_list = [{'_id': ['212.129.5.0','212.129.5.255'],
                       'objects': ['observable1', 'observable2']},
                      {'_id': ['213.129.5.0','213.129.5.255'],
                       'objects': ['observable10', 'observable20']}]

    address_id_list_result = [{"212.129.5.0 - 212.129.5.255": ['observable1','observable2']},
                            {"213.129.5.0 - 213.129.5.255": ['observable10','observable20']}]

    hash_array = [{'_id': 'MD5',
                    'objects': ['observable1', 'observable2','observable3']},
                     {'_id': 'SHA512',
                     'objects': ['observable10', 'observable20']}]

    hash_array_result = [{'MD5': ['observable1', 'observable2','observable3']},
                         {'SHA512': ['observable10', 'observable20']}]

    hash_array_plain_text = "MD5 - observable1, observable2, observable3" +"\n" + "SHA512 - observable10, observable20" + "\n"

    def test_correct_matches_array_list_id(self):
       self.assertEqual(generate_matches_array(self.address_id_list), self.address_id_list_result)

    def test_correct_matches_array_no_list_id(self):
        self.assertEqual(generate_matches_array(self.hash_array), self.hash_array_result)

    def test_correct_plain_text_response(self):
        self.assertEqual(plain_text_response(self.hash_array_result), self.hash_array_plain_text)
