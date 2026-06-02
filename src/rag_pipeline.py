import os
from pathlib import Path
import chromadb
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_DIR = "data"
DB_DIR = "chroma_db"
COLLECTION_NAME = "mauricio_knowledge_base"


def load_markdown_files(data_dir=DATA_DIR):
    documents = []

    for file_path in Path(data_dir).rglob("*.md"):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

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
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_vector_database():
    chroma_client = chromadb.PersistentClient(path=DB_DIR)

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = load_markdown_files()

    ids = []
    texts = []
    metadatas = []
    embeddings = []

    counter = 0

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
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

    return f"Vector database created with {counter} chunks."


def search_knowledge_base(question, n_results=5):
    chroma_client = chromadb.PersistentClient(path=DB_DIR)

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results


def generate_answer(question):
    results = search_knowledge_base(question)

    retrieved_chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are Mauricio Ruiz's AI career assistant.

Answer the user's question using only the provided context.
If the answer is not in the context, say that the information is not available.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant for Mauricio's CV and portfolio."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return answer, sources
