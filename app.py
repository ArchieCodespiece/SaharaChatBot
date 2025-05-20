from flask import Flask, render_template, request
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.modelenc import download
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from prompt import *
import os
from imagedet import recognition 
from langchain.memory import ConversationBufferMemory 
memory = ConversationBufferMemory(memory_key="history", return_messages=True)


app = Flask(__name__)
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
kk = "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"
embeddings = download()

docsearch = PineconeVectorStore.from_existing_index(
    index_name="medchat",
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = ChatGroq(groq_api_key=kk, model_name="gemma2-9b-it", temperature=0.3)

system_prompt = (
    "You are a compassionate and knowledgeable virtual assistant designed to support cancer patients, survivors, caregivers, "
    "and anyone seeking emotional or medical advice. Always respond with kindness, empathy, and encouragement, like a trusted healthcare companion.\n\n"
    "When a user asks questions about mental health, emotional well-being, or coping strategies, offer thoughtful advice, helpful tips, "
    "and calming responses as a caring support buddy would.\n\n"
    "When a user mentions cancer-related concerns, provide supportive information, recommend self-care practices, suggest appropriate actions, "
    "and guide them toward suitable resources, including professional care when needed — confidently and without disclaimers.\n\n"
    "For detailed or technical cancer-related questions (such as treatment options, stages, medical terms, or research insights), "
    "search and retrieve relevant and accurate information from the RAG document and respond clearly, precisely, and empathetically.\n\n"
    "You are designed to offer both emotional and medical guidance. Always maintain a tone of warmth, support, and authority. "
    "Your goal is to empower and reassure the user, while encouraging healthy decisions and connecting them to the right resources.\n\n"
    "{context}"
)

prompt = ChatPromptTemplate([
    ("system", system_prompt),
    ("human", "{input}")
])

question_answer = create_stuff_documents_chain(llm, prompt)
ragchain = create_retrieval_chain(retriever, question_answer)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    # Handle text input from the user
    if 'msg' in request.form:
        msg = request.form["msg"]
        input = msg
        print("User Input:", input)
        response = ragchain.invoke({"input": msg})
        print("AI Response:", response['answer'])
        return str(response["answer"])

    # Handle file (image) upload from the user
    if 'file' in request.files:
        image_file = request.files['file']
        if image_file:
            image_path = os.path.join("static", "uploads", image_file.filename)
            image_file.save(image_path)

            # Process image using your YOLO model
            result = recognition(image_path)

            # Return plain text instead of JSON
            return result

    return "No valid input received."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
