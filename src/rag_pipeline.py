import hashlib
import json
import os
from pathlib import Path

import chromadb
from google import genai
from sentence_transformers import SentenceTransformer


DATA_DIR = "data"
DB_DIR = "chroma_db"
COLLECTION_NAME = "mauricio_knowledge_base"
HASH_FILE = "chroma_db/content_hash.json"

LOCAL_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_api_key():
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")


api_key = get_api_key()

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to Streamlit secrets or as an environment variable."
    )

gemini_client = genai.Client(api_key=api_key)
local_embedding_model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)


def calculate_content_hash():
    combined_text = ""

    for file_path in sorted(Path(DATA_DIR).rglob("*.md")):
        combined_text += str(file_path)
        combined_text += file_path.read_text(encoding="utf-8")

    return hashlib.md5(combined_text.encode("utf-8")).hexdigest()


def database_needs_rebuild():
    current_hash = calculate_content_hash()

    if not os.path.exists(HASH_FILE):
        return True

    with open(HASH_FILE, "r", encoding="utf-8") as f:
        saved_hash = json.load(f).get("content_hash")

    return current_hash != saved_hash


def save_content_hash():
    os.makedirs(DB_DIR, exist_ok=True)

    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump({"content_hash": calculate_content_hash()}, f)


def load_markdown_files():
    documents = []

    for file_path in sorted(Path(DATA_DIR).rglob("*.md")):
        text = file_path.read_text(encoding="utf-8").strip()

        if text:
            documents.append({
                "text": text,
                "source": str(file_path)
            })

    return documents


def get_embedding(text):
    try:
        response = gemini_client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return response.embeddings[0].values

    except Exception:
        return local_embedding_model.encode(text).tolist()


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

    documents = load_markdown_files()

    for counter, doc in enumerate(documents):
        ids.append(f"doc_{counter}")
        texts.append(doc["text"])
        metadatas.append({"source": doc["source"]})
        embeddings.append(get_embedding(doc["text"]))

    if not ids:
        raise ValueError("No markdown files found in the data folder.")

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    save_content_hash()

    return f"Knowledge base created with {len(ids)} documents."


def search_knowledge_base(question, n_results=6):
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

    prompt = f"""
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
