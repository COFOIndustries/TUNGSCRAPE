import requests
from bs4 import BeautifulSoup
import re
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tungscrape_db']  # Database name
collection = db['media_files']  # Collection name

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
                
                # Insert the media data into MongoDB if not a duplicate
                if not collection.find_one({"url": media_url}):
                    collection.insert_one(media_info)
                    print(f"Added to MongoDB: {media_info}")
                else:
                    print(f"Already exists in MongoDB: {media_url}")

        return media_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    website_url = input("Enter the website URL to scrape: ")
    scrape_website(website_url)
