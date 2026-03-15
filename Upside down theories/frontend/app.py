import streamlit as st
import sys
import os

# ---------------------------------------------------
# Fix project path
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Import backend modules
from backend.rag_engine import (
    load_documents,
    split_documents,
    create_vector_database,
    ask_question
)

from backend.slide_planner import (
    generate_slide_content,
    parse_slides
)

from backend.slide_generator import create_presentation
from backend.html_slide_generator import create_html_slides

from langchain_ollama import OllamaLLM


# ---------------------------------------------------
# Initialize LLM
# ---------------------------------------------------

llm = OllamaLLM(model="mistral")


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------

st.set_page_config(page_title="Mr Clarke Briefing Generator")

st.title("Mr Clarke Automated Briefing Generator")

st.write("Upload documents and generate AI briefing slides.")


# ---------------------------------------------------
# Ensure folders exist
# ---------------------------------------------------

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Upload PDF
# ---------------------------------------------------

uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

if uploaded_file:

    file_path = os.path.join(DATA_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Document uploaded successfully!")


# ---------------------------------------------------
# Build Knowledge Base
# ---------------------------------------------------

if st.button("Build Knowledge Base"):

    with st.spinner("Loading and indexing documents..."):

        docs = load_documents()

        chunks = split_documents(docs)

        vector_db = create_vector_database(chunks)

        st.session_state.vector_db = vector_db

    st.success("Knowledge base ready!")


# ---------------------------------------------------
# Ask Question
# ---------------------------------------------------

question = st.text_input("Ask a question to generate briefing")

if st.button("Generate Briefing"):

    if "vector_db" not in st.session_state:

        st.error("Please build the knowledge base first!")

    else:

        with st.spinner("Generating AI briefing..."):

            vector_db = st.session_state.vector_db

            answer, sources = ask_question(vector_db, question)

        st.subheader("AI Generated Answer")

        st.write(answer)

        # ---------------------------------------------------
        # AI Slide Generation
        # ---------------------------------------------------

        slide_text = generate_slide_content(llm, answer)

        slides = parse_slides(slide_text)

        create_presentation(question, slides, sources)
        html_path = create_html_slides(question, slides)

        ppt_path = os.path.join(OUTPUT_DIR, "briefing.pptx")

        st.success("Presentation generated!")

        # ---------------------------------------------------
        # Download PPT
        # ---------------------------------------------------

        with open(ppt_path, "rb") as f:

            st.download_button(
                label="Download Presentation",
                data=f,
                file_name="briefing.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        with open(html_path, "rb") as f:

            st.download_button(
                label="Download Animated HTML Slides",
                data=f,
                file_name="briefing.html",
                mime="text/html"
            )