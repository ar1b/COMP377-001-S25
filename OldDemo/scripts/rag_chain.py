import os
from dotenv import load_dotenv

# ✅ Updated imports based on LangChain >= 0.1.16
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Loads environment variables from .env file (e.g., GOOGLE_API_KEY and GEMINI_API_KEY), 
# in this folder or parent folder
# This allows LangChain to use Gemini (GoogleGenerativeAI) without hardcoding the key
load_dotenv()

# ✅ Build vectorstore from absolute data/ path
def build_vectorstore():
    # Locate data folder relative to this script's parent
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder = os.path.join(base_dir, "data")

    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"[ERROR] data folder not found at: {data_folder}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_docs = []

    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            path = os.path.join(data_folder, filename)
            loader = TextLoader(path)
            docs = loader.load_and_split(text_splitter)
            all_docs.extend(docs)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # create FAISS vectorstore from documents and embeddings
    db = FAISS.from_documents(all_docs, embeddings)
    return db

# ✅ Explicit prompt for Gemini-powered RAG
prompt_template = """You are a therapy chatbot. Not a real therapist.

Context:
{context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# ✅ Full RAG pipeline using Gemini + FAISS
def get_rag_chain():
    vectorstore = build_vectorstore()
    retriever = vectorstore.as_retriever()

    llm = GoogleGenerativeAI(model="gemini-1.5-flash")  # Or gemini-2.0-flash if available

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )
    return chain
