import os


class Prompt:
    """Class to handle prompt template and formatting"""

    def __init__(self, template_path=None, second_template_path=None):
        """Initialize with optional custom template paths"""
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__), 'prompt_template.txt')
        if second_template_path is None:
            second_template_path = os.path.join(
                os.path.dirname(__file__), 'prompt_template2.txt')
        self.template_path = template_path
        self.second_template_path = second_template_path

    def set_template_path(self, path: str) -> None:
        """Set a custom template path"""
        if not os.path.exists(path):
            raise ValueError(f"Template file not found: {path}")
        self.template_path = path

    def format(self, text, metadata=None):
        """Format the first prompt with given text and metadata"""
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

    def format_second(self, text):
        """Format the second prompt with given text"""
        # Read the second template file
        with open(self.second_template_path, 'r') as f:
            prompt = f.read()

        # Replace placeholder
        prompt = prompt.replace('{text}', text)

        return prompt
