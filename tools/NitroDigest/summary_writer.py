import os
import yaml
from datetime import datetime
import re


class SummaryWriter:
    """Handles writing summaries to files with proper formatting"""
    
    def __init__(self, output_dir=None):
        """Initialize the summary writer"""
        self.output_dir = output_dir or os.environ.get("SUMMARIES_PATH", "summaries")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def write_summary(self, summary, metadata):
        """Write a summary to a markdown file with YAML frontmatter"""
        if not summary or not metadata:
            return None
        
        try:
            # Generate filename from subject or date
            filename = self._generate_filename(metadata)
            filepath = os.path.join(self.output_dir, filename)
            
            # Prepare YAML frontmatter
            frontmatter = {
                'title': metadata.get('subject', 'Untitled Newsletter'),
                'source': metadata.get('from', 'Unknown'),
                'date': metadata.get('date', datetime.now().strftime("%Y-%m-%d")),
                'email_id': metadata.get('id', ''),
                'summary_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Write to file with YAML frontmatter
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('---\n')
                yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
                f.write('---\n\n')
                f.write(summary)
            
            print(f"Summary written to {filepath}")
            return filepath
        
        except Exception as e:
            print(f"Error writing summary file: {e}")
            return None
    
    def _generate_filename(self, metadata):
        """Generate a filename based on the subject and date"""
        subject = metadata.get('subject', 'Untitled')
        date_str = None
        
        # Try to parse date from metadata
        if 'date' in metadata:
            try:
                # This is a simple approach - more sophisticated date parsing might be needed
                date_match = re.search(r'\d{1,2}\s+\w+\s+\d{4}', metadata['date'])
                if date_match:
                    date_str = date_match.group(0).replace(' ', '-')
            except:
                pass
        
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Clean the subject for use as a filename
        clean_subject = re.sub(r'[^\w\s-]', '', subject)
        clean_subject = re.sub(r'\s+', '-', clean_subject).strip('-').lower()
        clean_subject = clean_subject[:50]  # Limit length
        
        return f"{date_str}-{clean_subject}.md"


# Example usage
def test_summary_writer():
    summary = """
# Tech Weekly Newsletter Summary

## AI Advances
- OpenAI released GPT-5 with improved reasoning and multimodal capabilities
- The new model processes images, audio, and text with higher accuracy

## Industry News
- Apple announced M3 Pro chips with 40% better performance and lower power consumption
- Google Cloud introduced new serverless database options for enterprise customers

## Upcoming Events
- Annual Developer Conference on May 15-17 in San Francisco
    """
    
    metadata = {
        'from': 'Tech Weekly <news@techweekly.com>',
        'subject': 'This Week in Tech - Issue #42',
        'date': 'Mon, 1 Apr 2025 09:30:00 -0700',
        'id': '12345'
    }
    
    writer = SummaryWriter(output_dir="test_summaries")
    filepath = writer.write_summary(summary, metadata)
    
    if filepath and os.path.exists(filepath):
        print(f"Success! Summary written to {filepath}")
        # Read the file back to verify
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\nFile content preview:")
            print(content[:500] + "..." if len(content) > 500 else content)
        
        # Clean up test file
        os.remove(filepath)
        if not os.listdir("test_summaries"):
            os.rmdir("test_summaries")
    else:
        print("Failed to write summary")


if __name__ == "__main__":
    test_summary_writer()
