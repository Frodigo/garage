import os


class Prompt:
    """Class to handle prompt template and formatting"""

    def __init__(self, template_path=None):
        """Initialize with optional custom template path"""
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__), 'prompt_template.txt')
        self.template_path = template_path

    def format(self, text, metadata=None):
        """Format the prompt with given text and metadata"""
        # Read the template file
        with open(self.template_path, 'r') as f:
            prompt = f.read()

        # Format metadata
        metadata_str = ""
        if metadata:
            metadata_str = (
                f"This email is from: {metadata.get('from', 'Unknown')}\n"
                f"Subject: {metadata.get('subject', 'Unknown')}\n"
                f"Date: {metadata.get('date', 'Unknown')}\n"
            )

        # Replace placeholders
        prompt = prompt.replace('{metadata}', metadata_str)
        prompt = prompt.replace('{text}', text)

        return prompt
