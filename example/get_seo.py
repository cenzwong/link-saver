import requests
from bs4 import BeautifulSoup
import argparse
import json

def get_seo_details(url, mode='txt'):
    if mode not in ['txt', 'json']:
        raise ValueError("Mode must be 'txt' or 'json'")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the SEO title
    title = soup.find('title').text if soup.find('title') else 'No title found'

    # Extract the SEO description
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else 'No description found'

    if mode == 'json':
        return json.dumps({'Title': title, 'Description': description}, indent=4)
    else:
        return f"Title: {title}\nDescription: {description}"

def main():
    parser = argparse.ArgumentParser(description="Get SEO title and description from a website")
    parser.add_argument('url', type=str, help='The URL of the website to analyze')
    parser.add_argument('--mode', type=str, choices=['txt', 'json'], default='txt', help='Output mode: txt or json')
    args = parser.parse_args()

    output = get_seo_details(args.url, args.mode)
    print(output)

if __name__ == "__main__":
    main()