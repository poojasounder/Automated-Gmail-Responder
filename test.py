""" 
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup
import re

def get_article(page):
   new_page = re.sub('<br />','  ', page)
   main = BeautifulSoup(new_page, "html.parser").find("div", {"id": "main"})
   if main:
    return(re.sub('[\n,\r]',' ', main.get_text()))

def get_url(url):
    loader = RecursiveUrlLoader(
        url = url,
        max_depth = 12,
        extractor=lambda x: get_article(x)
    )
    docs = loader.load()
    return(docs)

scraped_docs = get_url("https://pdx.smartcatalogiq.com/en/2023-2024/bulletin/maseeh-college-of-engineering-and-computer-science/computer-science/")
scraped_docs.extend(get_url("https://pdx.smartcatalogiq.com/en/2023-2024/bulletin/courses/cs-computer-science/"))

print(f"Downloaded and parsed {len(scraped_docs)}")
for d in scraped_docs:
    print(d.metadata['source']) """
""" from langchain import hub
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(
            instructions="Answer the user's request utilizing at most 8 tool calls"
        )
print(prompt.template) """
""" from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import Html2TextTransformer

# Function to extract visible text from HTML
def extract_visible_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    [s.extract() for s in soup(['header','script', 'style', 'footer'])]  # Remove script and style tags
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        link_text = link.get_text(strip=True)
        links.append((href, link_text))
    # Print extracted links
    for link_text, href in links:
        print(f"{link_text}: {href}")
    visible_text = soup.get_text(separator=' ', strip=True)  # Get visible text
    return visible_text

# Fetch HTML content from URL
url = "https://www.pdx.edu/computer-science/computer-science-courses"
response = requests.get(url)
html_content = response.text

# Extract visible text
visible_text = extract_visible_text(html_content)
print(visible_text)  """
from bs4 import BeautifulSoup
import requests
import re
# Function to extract visible text from HTML
def extract_visible_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    [s.extract() for s in soup(['header','script', 'style', 'footer'])]  # Remove script and style tags
    
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
url = "https://www.pdx.edu/computer-science/computer-science-courses"
response = requests.get(url)
html_content = response.text

# Extract visible text
visible_text = extract_visible_text(html_content)
print(visible_text)

""" from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Function to extract text content and full URLs from HTML
def extract_text_and_full_urls(html_content,base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements like header, script, and style
    [s.extract() for s in soup(['header', 'script', 'style', 'footer'])]
    
    # Extract text content and full URLs
    text_and_urls = []
    for li_tag in soup.find_all('li'):
        a_tag = li_tag.find('a')
        if a_tag and 'computer-science' in a_tag.get('href'):
            text = a_tag.get_text().strip()
            href = a_tag.get('href')
            full_url = urljoin(base_url, href)
            text_and_urls.append((text, full_url))
        else :
            text = a_tag.get_text().strip()
            href = a_tag.get('href')
            text_and_urls.append((text, href))
    
    return text_and_urls

# Fetch HTML content from URL
url = "https://www.pdx.edu/computer-science/computer-science-courses"
response = requests.get(url)
html_content = response.text

base_url = "https://www.pdx.edu"
# Extract text content and full URLs
text_and_urls = extract_text_and_full_urls(html_content,base_url)

# Now 'text_and_urls' contains tuples of text content and corresponding href attributes
# You can print or use this data in your application
print("Text Content and Href Attributes:")
for text, href in text_and_urls:
    print(f"Text: {text}, Href: {href}") """

""" from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Function to extract visible text and links from HTML
def extract_visible_text_with_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    [s.extract() for s in soup(['script', 'style', 'header', 'footer'])]  # Remove script and style tags
    
    visible_text = ""
    for li_tag in soup.find_all('li'):
        tag = li_tag.find('a')
        if tag :
            visible_text += f"{tag.text} ({urljoin(base_url, tag['href'])}) "  # Append link text and href
        else:
            visible_text += f"{tag.text} "  # Append text of other tags

    return visible_text.strip()  # Remove leading and trailing spaces

# Fetch HTML content from URL
url = "https://www.pdx.edu/computer-science/computer-science-courses"
response = requests.get(url)
html_content = response.text

# Extract visible text with links
visible_text_with_links = extract_visible_text_with_links(html_content, url)
print(visible_text_with_links) """

# Optionally, save the visible text with links to a file
# with open("visible_text_with_links.txt", "w") as file:
#     file.write(visible_text_with_links)
""" 
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
# Function to extract visible text with links and without header and footer from HTML
def extract_visible_text_with_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    [s.extract() for s in soup(['header','script','style', 'footer'])]  # Remove header and footer tags
    
    visible_text = ""
    for tag in soup.find_all():
        if tag.name == 'a' and 'computer-science' in tag.get('href'):
            visible_text += f"{tag.text.strip()} ({urljoin(base_url, tag['href'])})\n" 
            print(visible_text)
        elif tag.name == 'a':
            visible_text += f"{tag.text.strip()} {tag.get('href')})\n"  # Append link text and href
            print(visible_text)
        else:
            visible_text += f"{tag.text.strip()}\n"  # Append text of other tags
            print(visible_text)

    return visible_text.strip()  # Remove leading and trailing newlines

# Fetch HTML content from URL
url = "https://www.pdx.edu/computer-science/computer-science-courses"
response = requests.get(url)
html_content = response.text
base_url = "https://www.pdx.edu"
# Extract visible text with links and without header and footer
visible_text_with_links = extract_visible_text_with_links(html_content, base_url)
print(visible_text_with_links) """

""" 
import requests
from bs4 import BeautifulSoup

def extract_text_and_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    [s.extract() for s in soup(['header','script','style', 'footer'])]
    # Remove empty or whitespace-only elements
    for elem in soup.find_all():
        if elem.text.strip() == "":
            elem.extract()
    # Extract text content
    text_content = soup.get_text().strip()
    
    # Extract links
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    
    return text_content, links

# Example usage
url = "https://www.pdx.edu/computer-science/computer-science-courses"
text_content, links = extract_text_and_links(url)
print("Text content:")
print(text_content)
print("\nLinks:")
print(links) """








