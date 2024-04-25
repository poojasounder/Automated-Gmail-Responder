from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

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

if __name__ == "__main__":
    response = requests.get("https://www.pdx.edu/computer-science/")
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    # Open a file in write mode
    with open("./Upload_documents/urls.txt", "w") as file:
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'computer-science' in href:
                full_url = urljoin("https://www.pdx.edu/computer-science/", href)
                file.write(full_url + "\n")
            

    # Fetch HTML content from URL
    url = "https://www.pdx.edu/computer-science/grad-prep"
    response = requests.get(url)
    html_content = response.text
    # Extract visible text
    visible_text = extract_visible_text(html_content)
    print(visible_text)
    #loader = TextLoader("./visible_text.txt")
    #data = loader.load()
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    #chunks = text_splitter.split_documents(data)
    #print(chunks)