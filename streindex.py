from src.modelenc import load, download, chunk


from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
exdata = load('goku.pdf')
textchunk = chunk(exdata)
embeddings = download()
docsearch = PineconeVectorStore.from_documents(
documents=textchunk,
index_name = "medchat",
embedding=embeddings
)
