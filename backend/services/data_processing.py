import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

def url_to_pdf(url: str) -> bool:
    '''Converts a URL to a PDF'''
    # TODO: convert url to pdf
    # TODO: store pdf on cloud (maybe google bucket?)
    # return True on success
    ...

def chunk_pdf(file_name: str, chunk_size=999, chunk_overlap=199) -> list[str]:
    '''Converts a PDF to a list of chunks'''
    # TODO: use google bucket url instead of local file
    file_path = os.path.join(os.path.dirname(__file__), f'documents/{file_name}')
    pdf_reader = PdfReader(stream=file_path)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function = len
        )
    chunks = text_splitter.split_text(text)
    return chunks
