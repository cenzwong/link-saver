import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json

import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Set your OpenAI API key

def fetch_website_content(url):
    """
    Fetch the raw HTML content of the website.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_text(html_content, max_chars=5000):
    """
    Extract visible text from HTML.
    Limit the extracted text to max_chars to keep prompt size manageable.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return text[:max_chars]

def get_website_descriptor(url, website_text):
    """
    Calls the LLM to get the website descriptor.
    The prompt instructs the model to identify:
      - 3 genres of the website,
      - 5 categories,
      - 10 potential tags,
      - What the website is for,
    and return the output in JSON format following:
    {
      "tags": ["tag1", "tag2", ...],
      "description": "I am the description of the website."
    }
    """
    prompt = (
        f"You are a descriptor of a website. Given the following website content from {url}:\n\n"
        f"{website_text}\n\n"
        "Identify:\n"
        "1. Three genres of the website.\n"
        "2. Five categories the website falls under.\n"
        "3. Ten potential tags associated with the website.\n"
        "4. A brief explanation of what the website is for.\n\n"
        "Provide the answer strictly in JSON format with the following schema:\n"
        '{\n'
        '  "tags": ["tag1", "tag2", ...],\n'
        '  "description": "I am the description of the website."\n'
        '}\n'
    )

    try:
        response = client.chat.completions.create(model="gpt-4o-mini-search-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        message_content = response.choices[0].message.content.strip()
        # Try parsing the output as JSON
        descriptor = json.loads(message_content)
        return descriptor
    except Exception as e:
        print(message_content)
        print(f"Error during LLM processing: {e}")
        return None

def main():
    url = input("Enter the website URL: ").strip()
    html_content = fetch_website_content(url)
    if not html_content:
        print("Failed to fetch website content.")
        return

    website_text = extract_text(html_content)
    descriptor = get_website_descriptor(url, website_text)

    if descriptor:
        print("Output JSON:")
        print(json.dumps(descriptor, indent=2))
    else:
        print("Failed to generate website descriptor.")

if __name__ == '__main__':
    main()
