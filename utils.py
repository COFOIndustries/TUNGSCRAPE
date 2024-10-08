import re

# Regex function to match media file types
def extract_file_type(url):
    file_types = re.findall(r'\.(mp4|mkv|mp3|avi|wav|mov)$', url)
    return file_types[0] if file_types else 'unknown'

# Function to clean up file names or titles
def clean_title(title):
    return re.sub(r'\s+', ' ', title).strip()
