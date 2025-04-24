from summary_writer import SummaryWriter
import unittest
import sys
import os
import tempfile
import shutil
from datetime import datetime


class TestSummaryWriter(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp()
        self.writer = SummaryWriter(output_dir=self.test_dir)

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_write_summary(self):
        summary = "# Test Summary\n\n- Point 1\n- Point 2\n"
        metadata = {
            'subject': 'Test Newsletter',
            'from': 'test@example.com',
            'date': 'Mon, 1 Apr 2025 10:00:00 -0700',
            'id': '12345'
        }

        filepath = self.writer.write_summary(summary, metadata)

        # Check that the file was created
        self.assertIsNotNone(filepath)
        assert filepath is not None  # Type narrowing
        self.assertTrue(os.path.exists(filepath))

        # Check file contents
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('title: Test Newsletter', content)
            self.assertIn('source: test@example.com', content)
            self.assertIn('# Test Summary', content)
            self.assertIn('- Point 1', content)
            self.assertIn('- Point 2', content)

    def test_write_summary_empty_inputs(self):
        # Test with empty summary
        result = self.writer.write_summary("", {'subject': 'Test'})
        self.assertIsNone(result)

        # Test with empty metadata
        result = self.writer.write_summary("Test summary", {})
        self.assertIsNone(result)

        # Test with None inputs
        result = self.writer.write_summary(None, None)
        self.assertIsNone(result)

    def test_generate_filename(self):
        # Test with subject and date
        metadata = {
            'subject': 'Test Newsletter: Special Edition!',
            'date': 'Mon, 1 Apr 2025 10:00:00 -0700'
        }
        filename = self.writer._generate_filename(metadata)
        self.assertIn('test-newsletter-special-edition', filename.lower())
        self.assertIn('1-apr-2025', filename)

        # Test with subject but no date
        metadata = {'subject': 'Test Newsletter'}
        filename = self.writer._generate_filename(metadata)
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, filename)
        self.assertIn('test-newsletter', filename.lower())


if __name__ == "__main__":
    unittest.main()
