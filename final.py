from bs4 import BeautifulSoup
import requests
import re
from langchain_community.document_loaders import TextLoader

from langchain_community.document_transformers import Html2TextTransformer
# Function to extract visible text from HTML
def extract_visible_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    [s.extract() for s in soup(['header','script', 'style', 'footer', 'nav'])]  # Remove script and style tags
    # Extract anchor tags and their href attributes
    links = {}
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        link_text = link.get_text(strip=True)
        links[href] = link_text
    
    # Extract visible text
    visible_text = soup.get_text(separator=' ', strip=True)  # Get visible text
    
    # Replace occurrences of href with href: corresponding link
    for href, link_text in links.items():
        visible_text = visible_text.replace(link_text, f"{link_text}: {href}")
    
    return visible_text

# Fetch HTML content from URL
url = "https://www.pdx.edu/academics/programs/undergraduate/computer-science"
response = requests.get(url)
html_content = response.text
visible_text = extract_visible_text(html_content)
file_path = "visible_text.txt"

# Open the file in write mode and save the visible text
with open(file_path, "w") as file:
    file.write(visible_text)
    
# Load the file as a text document
document_loader = TextLoader("./visible_text.txt")
document = document_loader.load()
print(document)



