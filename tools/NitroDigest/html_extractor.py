from bs4 import BeautifulSoup
import re


def extract_text_from_html(html_content):
    """Extract text from HTML content while maintaining some structure"""
    if not html_content:
        return ""

    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text(separator='\n', strip=True)

    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)

    return text


def test_html_extractor():
    """Test the HTML extractor with a simple HTML document"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Document</title>
        <style>
            body { font-family: Arial; }
        </style>
    </head>
    <body>
        <h1>Newsletter Title</h1>
        <p>This is a paragraph with <strong>important</strong> information.</p>
        <script>console.log('This should be removed');</script>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </body>
    </html>
    """

    extracted_text = extract_text_from_html(html)
    print("Extracted text:")
    print(extracted_text)


if __name__ == "__main__":
    test_html_extractor()
