import os

from backend.slide_generator import create_presentation
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM


# --------------------------------------------------
# STEP 1 — LOAD DOCUMENTS
# --------------------------------------------------

def load_documents():

    folder_path = "data"
    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            file_path = os.path.join(folder_path, file)

            loader = PyPDFLoader(file_path)

            docs = loader.load()

            documents.extend(docs)

    return documents


# --------------------------------------------------
# STEP 2 — SPLIT DOCUMENTS
# --------------------------------------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    return chunks


# --------------------------------------------------
# STEP 3 — CREATE VECTOR DATABASE
# --------------------------------------------------

def create_vector_database(chunks):

    embeddings = OllamaEmbeddings(model="mistral")

    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_db


# --------------------------------------------------
# STEP 4 — QUESTION ANSWERING
# --------------------------------------------------

def ask_question(vector_db, question):

    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 10
        }
    )

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    sources = [
        f"{doc.metadata.get('source')} (page {doc.metadata.get('page')})"
        for doc in docs
    ]

    llm = OllamaLLM(model="mistral")

    prompt = f"""
You are an assistant that answers ONLY using the provided context.

Use the context to explain clearly.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response, sources

def convert_to_slides(answer):

    slides = {
        "Overview": answer[:200],
        "Key Details": answer[200:400],
        "Conclusion": answer[400:600]
    }

    return slides
# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    print("\nLoading documents...\n")

    docs = load_documents()

    print("Documents loaded:", len(docs))


    print("\nSplitting documents into chunks...\n")

    chunks = split_documents(docs)

    print("Chunks created:", len(chunks))


    print("\nCreating vector database...\n")

    vector_db = create_vector_database(chunks)

    print("\nRAG system ready!\n")


    while True:

      question = input("\nEnter briefing topic (or exit): ")

      if question.lower() == "exit":
        break

      answer = ask_question(vector_db, question)

      slides = convert_to_slides(answer)

      create_presentation(question, slides)

      print("\nBriefing generated in output/briefing.pptx\n")

