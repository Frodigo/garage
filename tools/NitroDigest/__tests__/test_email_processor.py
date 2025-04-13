from email_processor import EmailProcessor
import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestEmailProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = EmailProcessor(
            'test@example.com', 'password', 'imap.example.com')

    @patch('imaplib.IMAP4_SSL')
    def test_connect_success(self, mock_imap):
        # Setup the mock
        mock_connection = MagicMock()
        mock_imap.return_value = mock_connection

        # Test
        result = self.processor.connect()

        # Verify
        self.assertTrue(result)
        mock_imap.assert_called_once_with('imap.example.com', 993)
        mock_connection.login.assert_called_once_with(
            'test@example.com', 'password')

    @patch('imaplib.IMAP4_SSL')
    def test_connect_failure(self, mock_imap):
        # Setup the mock to raise an exception
        mock_imap.side_effect = Exception("Connection failed")

        # Test
        result = self.processor.connect()

        # Verify
        self.assertFalse(result)

    def test_decode_email_header(self):
        # Basic header
        result = self.processor._decode_email_header("Simple header")
        self.assertEqual("Simple header", result)

        # Empty header
        result = self.processor._decode_email_header(None)
        self.assertEqual("", result)


if __name__ == "__main__":
    unittest.main()
