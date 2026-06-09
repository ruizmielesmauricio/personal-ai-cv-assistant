import hashlib
import json
import os
from pathlib import Path

import chromadb
from google import genai
from groq import Groq
from sentence_transformers import SentenceTransformer


DATA_DIR = "data"
DB_DIR = "chroma_db"
COLLECTION_NAME = "mauricio_knowledge_base"
HASH_FILE = "chroma_db/content_hash.json"

LOCAL_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_secret_or_env(key):
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return os.getenv(key)


gemini_api_key = get_secret_or_env("GEMINI_API_KEY")
groq_api_key = get_secret_or_env("GROQ_API_KEY")

if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to Streamlit secrets or environment variables."
    )

gemini_client = genai.Client(api_key=gemini_api_key)
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

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


def search_knowledge_base(question, n_results=3):
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


def build_prompt(question, context):
    return f"""
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


def generate_with_gemini(prompt):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_with_groq(prompt):
    if not groq_client:
        raise ValueError("GROQ_API_KEY not found. Groq fallback is unavailable.")

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Mauricio Ruiz's AI CV and portfolio assistant. "
                    "Answer professionally using only the provided context. "
                    "Do not invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content


def generate_context_fallback(context, gemini_error=None, groq_error=None):
    technical_details = ""

    if gemini_error:
        technical_details += f"\nGemini error: {gemini_error}"

    if groq_error:
        technical_details += f"\nGroq error: {groq_error}"

    return f"""
I could not generate a polished AI response at the moment, but the portfolio search worked.

Here is the most relevant information found in Mauricio's portfolio database:

{context}

Technical details:
{technical_details}
"""


def generate_answer(question):
    results = search_knowledge_base(question)

    chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(chunks)
    prompt = build_prompt(question, context)

    try:
        answer = generate_with_gemini(prompt)
        return answer, sources

    except Exception as gemini_error:
        try:
            answer = generate_with_groq(prompt)
            return answer, sources

        except Exception as groq_error:
            fallback_answer = generate_context_fallback(
                context=context,
                gemini_error=gemini_error,
                groq_error=groq_error
            )

            return fallback_answer, sources


def test_gemini():
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello in one short sentence."
    )

    return response.text
