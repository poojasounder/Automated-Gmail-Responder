from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from bs4 import BeautifulSoup

loader = PDFMinerPDFasHTMLLoader("./Upload_documents/Frequently Asked Questions (FAQ) - CS Graduate Admissions.pdf")
documents = loader.load()[0]
soup = BeautifulSoup(documents.page_content,'html.parser')
content = soup.find_all('div')
import re
cur_fs = None
cur_text = ''
snippets = []   # first collect all snippets that have the same font size
for c in content:
    sp = c.find('span')
    if not sp:
        continue
    st = sp.get('style')
    if not st:
        continue
    fs = re.findall('font-size:(\d+)px',st)
    if not fs:
        continue
    fs = int(fs[0])
    if not cur_fs:
        cur_fs = fs
    if fs == cur_fs:
        cur_text += c.text
    else:
        snippets.append((cur_text,cur_fs))
        cur_fs = fs
        cur_text = c.text
snippets.append((cur_text,cur_fs))
# Note: The above logic is very straightforward. One can also add more strategies such as removing duplicate snippets (as
# headers/footers in a PDF appear on multiple pages so if we find duplicates it's safe to assume that it is redundant info)
from langchain_community.docstore.document import Document
cur_idx = -1
semantic_snippets = []
# Assumption: headings have higher font size than their respective content
for s in snippets:
    # if current snippet's font size > previous section's heading => it is a new heading
    if not semantic_snippets or s[1] > semantic_snippets[cur_idx].metadata['heading_font']:
        metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
        metadata.update(documents.metadata)
        semantic_snippets.append(Document(page_content='',metadata=metadata))
        cur_idx += 1
        continue

    # if current snippet's font size <= previous section's content => content belongs to the same section (one can also create
    # a tree like structure for sub sections if needed but that may require some more thinking and may be data specific)
    if not semantic_snippets[cur_idx].metadata['content_font'] or s[1] <= semantic_snippets[cur_idx].metadata['content_font']:
        semantic_snippets[cur_idx].page_content += s[0]
        semantic_snippets[cur_idx].metadata['content_font'] = max(s[1], semantic_snippets[cur_idx].metadata['content_font'])
        continue

    # if current snippet's font size > previous section's content but less than previous section's heading than also make a new
    # section (e.g. title of a PDF will have the highest font size but we don't want it to subsume all sections)
    metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
    metadata.update(documents.metadata)
    semantic_snippets.append(Document(page_content='',metadata=metadata))
    cur_idx += 1
# Split the text into individual lines
lines = semantic_snippets[0].page_content.strip().split('\n')
# Initialize variables to store questions and answers
questions = []
answers = []
current_chunk = ""

# Loop through each line in the text
for line in lines:
    # Check if the line is empty or contains only whitespace
    if line.strip() == "":
        # If the current chunk is not empty, add it to either questions or answers
        if current_chunk:
            if "?" in current_chunk:
                questions.append(current_chunk.strip())
            else:
                answers.append(current_chunk.strip())
        current_chunk = ""  # Reset the current chunk
    else:
        # Concatenate the current line to the current chunk
        current_chunk += " " + line.strip()
        print(current_chunk)

# If there is remaining content in the current chunk, add it to either questions or answers
if current_chunk:
    if "?" in current_chunk:
        questions.append(current_chunk.strip())
    else:
        answers.append(current_chunk.strip())

# Combine questions and answers into chunks
chunks = [(q, a) for q, a in zip(questions, answers)]

# Print the chunks
for idx, chunk in enumerate(chunks, start=1):
    print(f"Chunk {idx}:")
    print("Question:", chunk[0])
    print("Answer:", chunk[1])
    print("\n")

