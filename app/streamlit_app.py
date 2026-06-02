import streamlit as st
from dotenv import load_dotenv
from rag_pipeline import build_vector_database, generate_answer

load_dotenv()

st.set_page_config(
    page_title="Mauricio AI CV Assistant",
    layout="wide"
)

st.title("Mauricio Ruiz — AI CV & Portfolio Assistant")

st.write(
    "Ask questions about my experience, skills, projects, education, and portfolio."
)

if st.button("Build / Refresh Knowledge Base"):
    with st.spinner("Building knowledge base..."):
        message = build_vector_database()
        st.success(message)

question = st.text_input("Ask a question")

if question:
    with st.spinner("Thinking..."):
        answer, sources = generate_answer(question)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources Used")
    for source in sources:
        st.write(source["source"])
