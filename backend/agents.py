from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
import os

db = None


# ✅ INGESTION
def ingestion_agent(file_path):
    global db

    try:
        print("📂 Processing:", file_path)

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        print("📄 Pages:", len(documents))

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        split_docs = splitter.split_documents(documents)

        print("✂️ Chunks:", len(split_docs))

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        db = FAISS.from_documents(split_docs, embeddings)

        print("✅ DB CREATED:", db is not None)

        return "Document processed successfully"

    except Exception as e:
        print("❌ ERROR:", e)
        return "Error in ingestion"


# ✅ SUMMARIZER
def summarizer_agent():
    global db

    if db is None:
        return "No document uploaded yet."

    docs = db.similarity_search("summarize", k=5)

    if not docs:
        return "No content found."

    content = " ".join([d.page_content for d in docs])

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    try:
        response = llm.invoke(f"Summarize:\n{content}")
        return response.content
    except Exception as e:
        print("❌ ERROR:", e)
        return "Error generating summary"

        response = llm.invoke(f"Summarize:\n{content}")
        return response.content

    except Exception as e:
        print("❌ ERROR:", e)
        return "Error generating summary"


# ✅ QA AGENT
def qa_agent(question):
    global db

    if db is None:
        return "No document uploaded yet."

    docs = db.similarity_search(question, k=3)
    context = " ".join([d.page_content for d in docs])

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    try:
        response = llm.invoke(f"Answer:\n{context}\n\nQ: {question}")
        return response.content
    except Exception as e:
        print("❌ ERROR:", e)
        return "Error generating answer"

        response = llm.invoke(f"Answer based on context:\n{context}\n\nQuestion: {question}")
        return response.content

    except Exception as e:
        print("❌ ERROR:", e)
        return "Error answering question"


# ✅ HIGHLIGHTS
def highlight_agent():
    global db

    if db is None:
        return []

    docs = db.similarity_search("important points", k=5)
    return [d.page_content[:200] for d in docs]