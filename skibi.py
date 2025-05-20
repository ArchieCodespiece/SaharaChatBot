# import os
# from langchain.chains import create_retrieval_chain
# from langchain_groq import ChatGroq
# from  langchain_core.prompts import ChatPromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
# from langchain_pinecone import PineconeVectorStore
# from dotenv import load_dotenv
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceBgeEmbeddings
# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# load_dotenv()

# os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# kk = "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"
# #loading the pdf
# def load(book):
#     loader = PyPDFLoader(book)
#     docs = loader.load()
#     return docs
# docs = load('goku.pdf')

# #chunking the pdf
# def chunk(data):
#     textsplt = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
#     textchunk = textsplt.split_documents(data)
#     return textchunk
# textchunk = chunk(docs)
# #starting of embeddings
# def download():
#     embeddings = HuggingFaceBgeEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
#     return embeddings
# embeddings = download()
# docsearch = PineconeVectorStore.from_documents(
# documents=textchunk,
# index_name = "skibi",
# embedding=embeddings
# )
# retriever = docsearch.as_retriever(search_type = "similarity",search_kwargs ={"k":3})
# # retrieveddocs = retriever.invoke("what is cancer?")
# # print(retrieveddocs)
# llm=ChatGroq(groq_api_key = kk,model_name ="gemma2-9b-it",temperature=0. )
# system_prompt = "you are helpful you will provide emotional support,answer cancer related queries,help people calm down and also answer out of context question{context}"
# prompt = ChatPromptTemplate(
#     [
#         ("system", system_prompt),
#         ("human","{input}")
#     ]
# )
# question_answer = create_stuff_documents_chain(llm, prompt)
# ragchain = create_retrieval_chain(retriever,question_answer)
# # res = ragchain.invoke({"input":"hello"})
# # print(res["answer"])

