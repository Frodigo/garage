import unittest
import sys
import os

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from html_extractor import extract_text_from_html


class TestHtmlExtractor(unittest.TestCase):
    
    def test_basic_html_extraction(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Document</title>
        </head>
        <body>
            <h1>Newsletter Title</h1>
            <p>This is a paragraph.</p>
        </body>
        </html>
        """
        
        result = extract_text_from_html(html)
        self.assertIn("Newsletter Title", result)
        self.assertIn("This is a paragraph", result)
    
    def test_script_style_removal(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>body { color: red; }</style>
        </head>
        <body>
            <h1>Title</h1>
            <script>alert('test');</script>
            <p>Content</p>
        </body>
        </html>
        """
        
        result = extract_text_from_html(html)
        self.assertIn("Title", result)
        self.assertIn("Content", result)
        self.assertNotIn("alert", result)
        self.assertNotIn("color: red", result)
    
    def test_empty_input(self):
        self.assertEqual("", extract_text_from_html(""))
        self.assertEqual("", extract_text_from_html(None))


if __name__ == "__main__":
    unittest.main()