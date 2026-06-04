# AI CV & Portfolio Assistant — Technical Report

## 1. Project Overview

This project implements an AI-powered CV and portfolio assistant using a Retrieval-Augmented Generation (RAG) architecture. The assistant allows users to ask questions about my experience, projects, skills, education, and career profile through an interactive Streamlit interface embedded in my GitHub Pages portfolio.

The application uses structured Markdown files as a knowledge base, retrieves relevant information using vector search, and generates natural-language answers using the Gemini API.

## 2. Objective

The objective was to build a portfolio-ready AI assistant that can:

* Answer questions about my professional experience.
* Explain my data analytics and machine learning projects.
* Highlight relevant technical skills.
* Support recruiters or hiring managers exploring my portfolio.
* Analyse job descriptions and suggest how my experience matches a role.

## 3. Architecture

The application follows a RAG pipeline:

```text
Markdown knowledge base
        ↓
Text chunking
        ↓
Gemini embeddings
        ↓
ChromaDB vector database
        ↓
User question
        ↓
Semantic search
        ↓
Relevant context retrieval
        ↓
Gemini response generation
        ↓
Streamlit chatbot interface
```

## 4. Project Structure

```text
personal-ai-cv-assistant/
├── app/
│   └── app.py
├── src/
│   ├── __init__.py
│   └── rag_pipeline.py
├── data/
│   ├── experience/
│   ├── projects/
│   ├── skills/
│   ├── education/
│   └── certifications/
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/secrets.toml
```

## 5. Knowledge Base

The knowledge base is stored in Markdown files inside the `data/` folder. These files contain structured information about:

* Work experience
* Data analytics projects
* Machine learning projects
* Technical skills
* Education
* Certifications
* Career goals

The use of Markdown makes the knowledge base easy to maintain, version-control, and update.

## 6. `app.py` — Streamlit Application

The `app.py` file controls the user interface.

### Main responsibilities

* Configures the Streamlit page.
* Loads the project root so files inside `src/` can be imported.
* Applies a SQLite compatibility patch for Streamlit Cloud deployment.
* Builds the vector database when the app starts.
* Displays a chatbot interface.
* Provides suggested question buttons.
* Includes a Job Description Analyzer tab.

### Main components

#### SQLite patch

```python
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass
```

This ensures ChromaDB works correctly in the Streamlit Cloud environment.

#### Project path setup

```python
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
```

This allows `app.py` to import Python modules from the `src/` folder.

#### Knowledge base initialization

```python
if "db_built" not in st.session_state:
    build_vector_database()
    st.session_state["db_built"] = True
```

This builds the vector database once per app session.

#### Chat interface

The app uses Streamlit chat components to create a conversational experience:

```python
st.chat_input()
st.chat_message()
```

User messages and assistant responses are stored in `st.session_state.messages` so the conversation remains visible during the session.

#### Suggested questions

The app includes pre-written question buttons to help visitors interact with the assistant easily.

Examples:

* What machine learning projects has Mauricio completed?
* Which projects demonstrate Python skills?
* Summarise Mauricio's experience as a Data Analyst.

#### Job Description Analyzer

The second tab allows users to paste a job description. The app compares the role requirements against the portfolio knowledge base and generates an evidence-based response.

## 7. `rag_pipeline.py` — RAG Pipeline

The `rag_pipeline.py` file contains the core retrieval and generation logic.

### Main responsibilities

* Loads Markdown files from the `data/` folder.
* Splits text into manageable chunks.
* Creates embeddings using Gemini.
* Stores embeddings in ChromaDB.
* Searches the vector database for relevant chunks.
* Sends the retrieved context to Gemini.
* Returns a grounded answer to the Streamlit app.

## 8. Data Loading

```python
for file_path in Path(DATA_DIR).rglob("*.md"):
```

The pipeline recursively scans the `data/` folder and loads every Markdown file.

Each document is stored with:

* The document text
* The file path as metadata

This makes it possible to track where retrieved information came from.

## 9. Text Chunking

```python
def chunk_text(text, chunk_size=1400, overlap=250):
```

Large documents are split into smaller chunks before being embedded.

The overlap ensures that important context is not lost between chunks.

Example:

```text
Chunk 1: characters 0–1400
Chunk 2: characters 1150–2550
Chunk 3: characters 2300–3700
```

This improves retrieval quality because the vector database searches smaller, focused sections rather than entire documents.

## 10. Embeddings

The project uses Gemini embeddings:

```python
model="gemini-embedding-001"
```

An embedding is a numerical representation of text. It allows the system to compare meaning rather than exact keywords.

For example, a question like:

```text
What Python experience does Mauricio have?
```

can retrieve content from project files mentioning:

* Python automation
* XGBoost
* Streamlit dashboards
* Data pipelines
* Machine learning workflows

even if the wording is different.

## 11. Vector Database

ChromaDB is used as the vector database.

It stores:

* Text chunks
* Embedding vectors
* Metadata such as source file paths

When a user asks a question, the question is also converted into an embedding. ChromaDB then finds the most semantically similar chunks.

## 12. Retrieval

```python
collection.query(
    query_embeddings=[question_embedding],
    n_results=8
)
```

The app retrieves the top 8 most relevant chunks from the knowledge base.

These chunks become the context used by Gemini to generate the final answer.

## 13. Gemini Response Generation

Gemini receives a prompt containing:

* The assistant role
* Instructions not to invent information
* Retrieved context
* The user question

The model is instructed to answer only using the retrieved context.

This reduces hallucination and ensures answers are grounded in the portfolio knowledge base.

## 14. Deployment

The app is deployed using Streamlit Cloud.

The Gemini API key is stored securely using Streamlit Secrets:

```toml
GEMINI_API_KEY = "..."
```

The API key is not stored in GitHub.

## 15. Portfolio Integration

The deployed Streamlit app is embedded into the GitHub Pages portfolio using an iframe:

```html
<iframe
  src="https://mauricio-ai-cv-assistant.streamlit.app/?embed=true"
  style="width: 100%; min-height: 900px; border: 1px solid #ddd; border-radius: 12px; background: white;"
  frameborder="0"
  scrolling="yes">
</iframe>
```

This allows visitors to interact with the assistant directly from the portfolio landing page.

## 16. Technologies Used

* Python
* Streamlit
* Gemini API
* Gemini Embeddings
* ChromaDB
* Markdown
* GitHub
* Streamlit Cloud
* GitHub Pages

## 17. Skills Demonstrated

* Retrieval-Augmented Generation
* Generative AI application development
* Vector databases
* Semantic search
* API integration
* Python development
* Streamlit deployment
* Personal knowledge base design
* Portfolio engineering
* Prompt engineering

## 18. Future Improvements

Potential future improvements include:

* Adding conversation memory across sessions.
* Improving the Job Description Analyzer with a match score.
* Adding downloadable CV improvement suggestions.
* Creating a source visibility toggle.
* Adding analytics to track common recruiter questions.
* Improving the UI design to match the portfolio branding.
* Adding support for multiple assistant personas, such as recruiter, hiring manager, or technical interviewer.

## 19. Conclusion

This project demonstrates how a personal career knowledge base can be transformed into an interactive AI assistant using RAG. Instead of relying only on a static CV or portfolio page, visitors can ask natural-language questions and receive targeted answers based on structured project and experience documentation.

The project combines data engineering, NLP, generative AI, vector search, and deployment into a practical portfolio application.
