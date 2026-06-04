from pathlib import Path

import chromadb
import streamlit as st
from google import genai
from sentence_transformers import SentenceTransformer


DATA_DIR = "data"
DB_DIR = "chroma_db"
COLLECTION_NAME = "mauricio_knowledge_base"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def load_markdown_files():
    documents = []

    for file_path in Path(DATA_DIR).rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "text": text,
            "source": str(file_path)
        })

    return documents


def chunk_text(text, chunk_size=1400, overlap=250):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def get_embedding(text):
    return embedding_model.encode(text).tolist()


def build_vector_database():
    chroma_client = chromadb.PersistentClient(path=DB_DIR)

    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = chroma_client.create_collection(COLLECTION_NAME)

    ids = []
    texts = []
    metadatas = []
    embeddings = []

    counter = 0

    for doc in load_markdown_files():
        for chunk in chunk_text(doc["text"]):
            ids.append(f"chunk_{counter}")
            texts.append(chunk)
            metadatas.append({"source": doc["source"]})
            embeddings.append(get_embedding(chunk))
            counter += 1

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return f"Knowledge base created with {counter} chunks."


def search_knowledge_base(question, n_results=8):
    chroma_client = chromadb.PersistentClient(path=DB_DIR)

    try:
        collection = chroma_client.get_collection(COLLECTION_NAME)
    except Exception:
        build_vector_database()
        collection = chroma_client.get_collection(COLLECTION_NAME)

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results


def generate_answer(question):
    results = search_knowledge_base(question)

    chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(chunks)

    prompt = prompt = f"""
You are Mauricio Ruiz's AI CV and portfolio assistant.

Your job is to answer like a strong career portfolio assistant.
Use specific evidence from the context.
Mention project names, tools, methods, results, and business impact when available.

Rules:
- Do not invent information.
- Do not answer generically.
- If the context contains relevant details, use them.
- If the question asks about experience, connect skills to specific projects or roles.
- If the question asks about suitability for a role, provide evidence-based reasoning.
- If information is missing, say what is missing.

Context:
{context}

Question:
{question}

Answer in a clear, professional style:
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text, sources

def test_gemini():
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello in one short sentence."
    )

    return response.text