import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from src.rag_pipeline import build_vector_database, generate_answer

import sys

try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass
    
st.set_page_config(
    page_title="Mauricio AI CV Assistant",
    layout="wide"
)

st.title("Mauricio Ruiz — AI CV & Portfolio Assistant")

st.write(
    "Ask questions about my experience, skills, projects, education, and portfolio."
)

if "db_built" not in st.session_state:
    with st.spinner("Preparing knowledge base..."):
        build_vector_database()
        st.session_state["db_built"] = True

if "messages" not in st.session_state:
    st.session_state.messages = []

tab1, tab2 = st.tabs([
    "Portfolio Assistant",
    "Job Description Analyzer"
])

with tab1:
    st.subheader("Ask my AI Portfolio Assistant")

    suggested_questions = [
        "What machine learning projects has Mauricio completed?",
        "Summarise Mauricio's experience as a Data Analyst.",
        "Which projects demonstrate Python skills?",
        "What experience does Mauricio have in machine learning?"
    ]

    cols = st.columns(2)

    selected_question = None

    for i, suggested_question in enumerate(suggested_questions):
        with cols[i % 2]:
            if st.button(suggested_question):
                selected_question = suggested_question

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    typed_question = st.chat_input(
        "Ask me about my experience, projects, or skills"
    )

    question = selected_question or typed_question

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Searching knowledge base and generating answer..."):
            answer, sources = generate_answer(question)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)

with tab2:
    st.subheader("Job Description Analyzer")

    st.write("Paste a job description here. This feature will analyse how well Mauricio's experience matches the role.")

    job_description = st.text_area(
        "Paste job description",
        height=250
    )

    if st.button("Analyze Job Description"):
        if job_description.strip():
            prompt = f"""
            Compare Mauricio's portfolio knowledge base against this job description.
            Identify relevant skills, matching projects, missing keywords, and suggested CV improvements.

            Job description:
            {job_description}
            """

            with st.spinner("Analysing job description..."):
                answer, sources = generate_answer(prompt)

            st.write(answer)
        else:
            st.warning("Please paste a job description first.")
