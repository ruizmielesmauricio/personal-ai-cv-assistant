from pathlib import Path
import requests
import chromadb
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
DB_DIR = "chroma_db"
COLLECTION_NAME = "mauricio_knowledge_base"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_markdown_files():
    documents = []

    for file_path in Path(DATA_DIR).rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "text": text,
            "source": str(file_path)
        })

    return documents


def chunk_text(text, chunk_size=900, overlap=150):
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


def search_knowledge_base(question, n_results=5):
    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    collection = chroma_client.get_collection(COLLECTION_NAME)

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results


def call_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    return response.json()["response"]


def generate_answer(question):
    results = search_knowledge_base(question)

    chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(chunks)

    prompt = f"""
You are Mauricio Ruiz's AI CV and portfolio assistant.

Answer the question using only the context below.
Do not invent information.
If the context does not contain the answer, say:
"I don't have enough information in the knowledge base to answer that."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = call_ollama(prompt)

    return answer, sources
