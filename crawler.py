""" from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-2125ef8c7b194e53b8c352d5e5797a34")

def crawl_recursive(url, params=None):
    # Crawl the given URL
    crawl_result = app.crawl_url(url, params=params)
    
    # Get the markdown for each crawled page
    for result in crawl_result:
        print(result['markdown'])
    
    # Extract links from the crawled page
    links = [link['url'] for result in crawl_result for link in result.get('links', [])]

    # Recursively crawl each extracted link
    for link in links:
        crawl_recursive(link, params=params)

# Start crawling from the main URL
main_url = 'https://www.pdx.edu/computer-science/'
params = {'crawlerOptions': { # leave empty for all pages
        'limit': 50,
    },
    'pageOptions': {
        'onlyMainContent': True
    }
}

crawl_recursive(main_url, params=params) """
import re

def split_text_into_chunks(text):
    # Define regular expressions for matching questions and answers
    question_pattern = r'Q: (.+?)\n'  # Matches lines starting with "Q: "
    answer_pattern = r'A: (.+?)\n'     # Matches lines starting with "A: "

    # Find all question and answer pairs using regular expressions
    qa_pairs = re.findall(question_pattern + answer_pattern, text, re.DOTALL)

    # If there are any remaining characters after extracting question-answer pairs,
    # treat them as a separate chunk
    remaining_text = re.sub(question_pattern + answer_pattern, '', text, flags=re.DOTALL).strip()
    if remaining_text:
        qa_pairs.append((remaining_text, ''))  # Append the remaining text as a separate chunk

    return qa_pairs

# Example usage
text = """
Q: What is the capital of France?
A: Paris
Q: Who wrote Hamlet?
A: William Shakespeare
This is some additional information.
"""

chunks = split_text_into_chunks(text)
for chunk in chunks:
    print(chunk)


