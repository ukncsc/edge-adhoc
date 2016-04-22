import unittest
from adapters.certuk_adhoc.query.cleanse_data import cleanse_data_list

class CleanseDataListTests(unittest.TestCase):

    input_duplicate = ['MD5', 'SHA112', 'MD5']
    output_duplicate = ['MD5', 'SHA112']

    input_whitespace = ['MD5    ', '   MD6', '   SHA112    ', '   ']
    output_whitespace = ['MD5', 'MD6', 'SHA112']

    input_duplicate_whitespace = ['MD5', '  MD5   ', '   ', '  SHA112', 'MD6  ']
    output_duplicate_whitespace = ['MD5', 'SHA112', 'MD6']

    input_nothing = ['  ', '    ']
    output_nothing = []

    def test_duplicate_entries_removed(self):
        self.assertEqual(cleanse_data_list(self.input_duplicate), self.output_duplicate)

    def test_whitespace_removed(self):
        self.assertEqual(cleanse_data_list(self.input_whitespace), self.output_whitespace)

    def test_duplicate_and_whitespace_removed(self):
        self.assertEqual(cleanse_data_list(self.input_duplicate_whitespace), self.output_duplicate_whitespace)

    def test_returns_empty_list(self):
        self.assertEqual(cleanse_data_list(self.input_nothing), self.output_nothing)
