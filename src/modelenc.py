from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
def load(book):
    loader = PyPDFLoader(book)
    docs = loader.load()
    return docs
def chunk(data):
    textsplt = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    textchunk = textsplt.split_documents(data)
    return textchunk
def download():
    embeddings = HuggingFaceBgeEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
    return embeddings