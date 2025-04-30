import imaplib
import email
from email.header import decode_header
from email.message import Message
import os
from html_extractor import extract_text_from_html
from typing import Optional, Union, List, Dict, Any, Tuple, Sequence
from dotenv import load_dotenv


class EmailProcessor:
    """Class for connecting to email server and processing emails"""

    def __init__(self, email_address: str, password: str, imap_server: str, imap_port: int = 993):
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self):
        """Connect to the IMAP server"""
        try:
            self.connection = imaplib.IMAP4_SSL(
                self.imap_server, self.imap_port)
            self.connection.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"Error connecting to email server: {e}")
            return False

    def disconnect(self):
        """Disconnect from the IMAP server"""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
            except:
                pass

    def get_unread_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch unread emails from specified folder"""
        if not self.connection:
            if not self.connect():
                return []
        assert self.connection is not None  # Type assertion

        try:
            self.connection.select(folder)
            status, messages = self.connection.search(None, '(UNSEEN)')

            if status != 'OK':
                return []

            email_ids = messages[0].split()
            # Limit the number of emails to process
            email_ids = email_ids[:limit] if limit else email_ids

            emails = []
            for email_id in email_ids:
                status, data = self.connection.fetch(email_id, '(RFC822)')
                if status != 'OK' or not data:
                    continue
                assert data is not None
                data_list = data

                raw_email = data_list[0][1] if isinstance(
                    data_list[0], tuple) else data_list[0]
                assert isinstance(raw_email, (bytes, bytearray))
                email_message: Message = email.message_from_bytes(raw_email)

                # Extract email content and metadata
                subject = self._decode_email_header(email_message['Subject'])
                from_address = self._decode_email_header(email_message['From'])
                date = email_message['Date']

                # Get the email body
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(
                            part.get("Content-Disposition"))

                        if "attachment" not in content_disposition:
                            if content_type == "text/plain":
                                payload = part.get_payload(decode=True)
                                assert isinstance(payload, (bytes, bytearray))
                                body = payload.decode()
                                break
                            elif content_type == "text/html" and not body:
                                payload = part.get_payload(decode=True)
                                assert isinstance(payload, (bytes, bytearray))
                                html = payload.decode()
                                body = extract_text_from_html(html)
                else:
                    content_type = email_message.get_content_type()
                    if content_type == "text/plain":
                        payload = email_message.get_payload(decode=True)
                        assert isinstance(payload, (bytes, bytearray))
                        body = payload.decode()
                    elif content_type == "text/html":
                        payload = email_message.get_payload(decode=True)
                        assert isinstance(payload, (bytes, bytearray))
                        html = payload.decode()
                        body = extract_text_from_html(html)

                # Add email to the list
                emails.append({
                    'id': email_id.decode(),
                    'subject': subject,
                    'from': from_address,
                    'date': date,
                    'body': body
                })

            return emails
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def _decode_email_header(self, header):
        """Decode email header"""
        if not header:
            return ""

        decoded_header = decode_header(header)
        header_parts = []

        for content, encoding in decoded_header:
            if isinstance(content, bytes):
                # If encoding is provided, use it, otherwise fallback to utf-8
                try:
                    if encoding:
                        content = content.decode(encoding)
                    else:
                        content = content.decode('utf-8')
                except:
                    # Fallback to utf-8 with errors ignored if decoding fails
                    content = content.decode('utf-8', errors='ignore')
            header_parts.append(str(content))

        return ' '.join(header_parts)

    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read"""
        if not self.connection:
            if not self.connect():
                return False
        assert self.connection is not None  # Type assertion

        try:
            self.connection.store(email_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            print(f"Error marking email as read: {e}")
            return False


# Example usage
def test_email_processor():
    # Get credentials from environment variables
    load_dotenv()
    email_address = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')
    imap_server = os.environ.get('IMAP_SERVER', 'imap.gmail.com')

    if not email_address or not password:
        print("Email credentials not found in environment variables")
        return

    processor = EmailProcessor(email_address, password, imap_server)
    emails = processor.get_unread_emails(limit=3)

    for i, email_data in enumerate(emails):
        print(f"\nEmail {i+1}:")
        print(f"Subject: {email_data['subject']}")
        print(f"From: {email_data['from']}")
        print(f"Date: {email_data['date']}")
        print(f"Body preview: {email_data['body'][:150]}...")

    processor.disconnect()


if __name__ == "__main__":
    test_email_processor()
