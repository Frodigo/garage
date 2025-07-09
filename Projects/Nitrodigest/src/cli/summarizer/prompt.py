import os


class Prompt:
    """Class to handle prompt template and formatting"""

    default_prompt = """You are an expert in research and summarization.
    Summarize the following text into a TL;DR list. **The summary *must* be formatted as a bulleted list,
    with each bullet point being a single, concise sentence.**
    Example:
    - Foo Unveils AR Platform, RealityOS
    - Integrates with existing devices and new lightweight AR glasses coming in September.
    - Bar Acquires AI Startup Nexus Minds
    - $3.8 billion deal for Toronto-based firm known for natural language processing.

    Content to summarize {metadata} {text}
"""

    def __init__(self, template_path=None):
        """Initialize with optional custom template path"""
        self.template_path = template_path

        if template_path and os.path.exists(template_path):
            with open(template_path, 'r') as f:
                self.prompt = f.read()
        else:
            self.prompt = self.default_prompt

    def set_template_path(self, path: str) -> None:
        """Set a custom template path"""
        if not os.path.exists(path):
            raise ValueError(f"Template file not found: {path}")
        self.template_path = path

    def get_prompt(self):
        """
        Get the raw prompt without formatting.

        Returns:
            str: The raw prompt with placeholders
        """
        return self.prompt

    def format(self, text, metadata=None):
        """Format the prompt with given text and metadata"""

        formatted_prompt = self.prompt

        # Format metadata
        metadata_str = ""
        if metadata:
            metadata_str = (
                f"Source: {metadata.get('from', 'Unknown')}\n"
                f"Subject: {metadata.get('subject', 'Unknown')}\n"
                f"Date: {metadata.get('date', 'Unknown')}\n"
            )

        # Replace placeholders
        formatted_prompt = formatted_prompt.replace('{metadata}', metadata_str)
        formatted_prompt = formatted_prompt.replace('{text}', text)

        return formatted_prompt
