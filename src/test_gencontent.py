import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a heading"
        self.assertEqual(extract_title(markdown), "This is a heading")
    
    def test_extract_title_longer_file(self):
        markdown = '''
        # This is a **heading**

        ## this is a sub_heading

        this is the **body** of the article
        '''
        self.assertEqual(extract_title(markdown), "This is a **heading**")
    
    def test_extract_title_raise_exception(self):
        markdown = '''
        ## This is a **heading**

        ### this is a sub_heading

        this is the **body** of the article
        '''
        with self.assertRaises(Exception):
            title = extract_title(markdown)
            