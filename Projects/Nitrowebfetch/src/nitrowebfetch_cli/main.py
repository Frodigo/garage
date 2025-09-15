import asyncio
import html2text
from argparse import ArgumentParser
from playwright.async_api import async_playwright


def main():
    parser = ArgumentParser(
        description="nitrowebfetch - Extract content from web pages using CSS selectors",
        epilog="Visit docs, if you need more information: https://frodigo.com/projects/Nitrowebfetch/README.md, or report issues: https://github.com/frodigo/garage/issues if something doesn't work as expected."
    )
    parser.add_argument(
        "url",
        help="URL to fetch content from"
    )
    parser.add_argument(
        "--selector",
        default="article",
        help="CSS selector to use for content extraction (default: article)"
    )

    parser.add_argument(
        "--format",
        default="md",
        help="Format of output content (default: md)"
    )

    args = parser.parse_args()

    asyncio.run(_fetch_page(args.url, args.selector, args.format))


async def _fetch_page(url, selector='article', format='md'):
    """
    Fetch specific content from a webpage using CSS selectors

    Args:
        url: The URL to scrape
        selector: CSS selector (default: 'article')
    """
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url)

            element = await page.query_selector(selector)
            if element:
                html_content = await element.inner_html()
                _render_output(html_content, format)
            else:
                print(f"No elements found matching selector: '{selector}'")

                # Try some common article selectors as alternatives
                alternatives = [
                    'article', 'main', '.article', '.content',
                    '#content', '.post', '.entry-content'
                ]

                for alt_selector in alternatives:
                    if alt_selector != selector:
                        alt_element = await page.query_selector(alt_selector)
                        if alt_element:
                            html_content = await alt_element.inner_html()
                            _render_output(html_content, format)
                            break

        except Exception as e:
            print(f"Error fetching page: {e}")
        finally:
            await browser.close()


def _render_output(html_content, format):
    if format == 'md':
        print(html2text.html2text(html_content))
        return

    print(html_content)
