import os
import requests
import json
from prompt import Prompt


class BaseSummarizer:
    """Base class for all summarizers"""
    
    def __init__(self):
        self.prompt = Prompt()
    
    def summarize(self, text, metadata=None):
        """Summarize the given text"""
        raise NotImplementedError("Subclasses must implement this method")


class ClaudeSummarizer(BaseSummarizer):
    """Summarizer that uses Anthropic's Claude API"""
    
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Claude API key is required")
    
    def summarize(self, text, metadata=None):
        """Summarize text using Claude API"""
        if not text:
            return ""
        
        try:
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            # Prepare prompt
            prompt = self.prompt.format(text, metadata)
            
            data = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 1000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code != 200:
                print(f"Error from Claude API: {response.status_code}")
                print(response.text)
                return ""
            
            response_data = response.json()
            return response_data["content"][0]["text"]
            
        except Exception as e:
            print(f"Error summarizing with Claude: {e}")
            return ""


class ChatGPTSummarizer(BaseSummarizer):
    """Summarizer that uses OpenAI's ChatGPT API"""
    
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    def summarize(self, text, metadata=None):
        """Summarize text using OpenAI API"""
        if not text:
            return ""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare prompt
            prompt = self.prompt.format(text, metadata)
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that summarizes newsletter content."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code != 200:
                print(f"Error from OpenAI API: {response.status_code}")
                print(response.text)
                return ""
            
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Error summarizing with ChatGPT: {e}")
            return ""


class OllamaSummarizer(BaseSummarizer):
    """Summarizer that uses a local Ollama instance"""
    
    def __init__(self, model="mistral", base_url="http://localhost:11434"):
        super().__init__()
        self.model = model
        self.base_url = base_url
    
    def summarize(self, text, metadata=None):
        """Summarize text using Ollama API"""
        if not text:
            return ""
        
        try:
            headers = {"Content-Type": "application/json"}
            
            # Prepare prompt
            prompt = self.prompt.format(text, metadata)
            
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code != 200:
                print(f"Error from Ollama API: {response.status_code}")
                print(response.text)
                return ""
            
            response_data = response.json()
            return response_data["response"]
            
        except Exception as e:
            print(f"Error summarizing with Ollama: {e}")
            return ""


# Example usage
def test_summarizer():
    # Test text
    text = """
    Welcome to our weekly tech newsletter!
    
    # Latest Updates
    
    ## AI Advances
    OpenAI has released GPT-5 with significant improvements in reasoning and multimodal capabilities.
    The new model can process images, audio, and text simultaneously with higher accuracy than previous versions.
    
    ## Industry News
    Apple announced their new M3 Pro chips that offer 40% better performance with lower power consumption.
    Google Cloud introduced new serverless database options for enterprise customers.
    
    # Tips & Tutorials
    Learn how to optimize your React applications with our step-by-step guide.
    
    # Upcoming Events
    Join us for the annual Developer Conference on May 15-17 in San Francisco.
    """
    
    metadata = {
        'from': 'Tech Weekly <news@techweekly.com>',
        'subject': 'This Week in Tech - Issue #42',
        'date': 'Mon, 1 Apr 2025 09:30:00 -0700'
    }
    
    # Try to use Claude if API key exists
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        print("Testing Claude summarizer...")
        summarizer = ClaudeSummarizer(api_key)
        summary = summarizer.summarize(text, metadata)
        print(summary)
    else:
        print("No Claude API key found, skipping Claude test")
    
    # Try to use ChatGPT if API key exists
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("\nTesting ChatGPT summarizer...")
        summarizer = ChatGPTSummarizer(api_key)
        summary = summarizer.summarize(text, metadata)
        print(summary)
    else:
        print("No OpenAI API key found, skipping ChatGPT test")
    
    # Try to use Ollama if it's running locally
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("\nTesting Ollama summarizer...")
            summarizer = OllamaSummarizer()
            summary = summarizer.summarize(text, metadata)
            print(summary)
        else:
            print("Ollama not running locally, skipping Ollama test")
    except:
        print("Ollama not running locally, skipping Ollama test")


if __name__ == "__main__":
    test_summarizer()
