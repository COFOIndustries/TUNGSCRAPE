import requests
from bs4 import BeautifulSoup
import re
import json

# Utility function to identify media files
def is_media_file(url):
    media_extensions = ['.mp4', '.mkv', '.mp3', '.wav', '.avi', '.mov']
    return any(url.endswith(ext) for ext in media_extensions)

# Function to scrape media files from a website
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'lxml')
        media_data = []

        # Extract all links from the webpage
        links = soup.find_all('a', href=True)

        for link in links:
            media_url = link['href']
            if is_media_file(media_url):
                # Get the title (if available)
                title = link.text.strip() or media_url.split('/')[-1]
                
                # Determine the file type
                file_type = media_url.split('.')[-1]

                # Save the media info in a structured format
                media_info = {
                    'title': title,
                    'url': media_url,
                    'file_type': file_type
                }
                media_data.append(media_info)

        return media_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Save scraped media data to a JSON file
def save_to_json(data, filename='data/scraped_media.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    website_url = input("Enter the website URL to scrape: ")
    media_data = scrape_website(website_url)
    
    if media_data:
        save_to_json(media_data)
    else:
        print("No media files found.")
