import unittest
from md_to_dict import MarkdownParser

class TestMarkdownParser(unittest.TestCase):

	def test_simple(self):
		md_parser = MarkdownParser('test_files/simple_valid.md')
		md_dict = md_parser.parse()
		self.assertEqual(md_dict['vendor']['vendor_website'], 'www.test.com')
		self.assertEqual(md_dict['data']['data_description'], 'awesome stuff')
		self.assertEqual(len(md_dict.keys()), 2)
		self.assertEqual(len(md_dict['vendor'].keys()), 2)
		self.assertEqual(len(md_dict['data'].keys()), 2)

if __name__ == '__main__':
    unittest.main()
