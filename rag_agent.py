''' To Run the App make sure You've called Deepseek via   Ollama, run Ollama via Ollama serve and then in a different terminal run streamlit run rag_agent.py'''
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import streamlit as st
import os
import logging

# session state variables
if "processed" not in st.session_state:
    st.session_state.processed = False
if "index" not in st.session_state:
    st.session_state.index = None

# Logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
st.set_page_config(page_title = "RAG Agent to Explore yor Document(s)", layout = "wide")

# Initializing Models
try:

    Settings.embed_model = HuggingFaceEmbedding(
        model_name = "BAAI/bge-small-en-v1.5"
    )
    Settings.llm = Ollama(model = "deepseek-llm", temperature = 0.1, request_timeout = 60.0)
    st.sidebar.success("Models Loaded Succesfully")
except Exception as e:
    st.sidebar.error("Model Loading Failed")

# App UI
st.title("Deepseek RAG Agent")
st.caption("Upload document(s) to ask questions (Permitted Docs are .pdf, .txt, .md, .docx, .pptx)")

# Create docs directory
os.makedirs("docs", exist_ok = True)

# File Uploader
with st.sidebar:
    st.subheader("Upload Document Here")
    uploaded_files = st.file_uploader(
        "Select Files",
        accept_multiple_files = True,
        type = ["pdf", "txt", "docx","pptx", "md"]
    )
    if uploaded_files:
        for file in uploaded_files:
            save_path = f"docs/{file.name}"
            with open(f"docs/{file.name}", "wb") as f:
                f.write(file.getbuffer())
            st.info(f"Saved: {file.name} ({os.path.getsize(save_path)/1024:.2f} KB)")
        
        st.success(f"Successfully Uploaded {len(uploaded_files)} file(s)")

        # Reset State
        st.session_state.processed = False
        st.session_state.index = None

# Processing and Q&A Section
if not st.session_state.processed:
    doc_files = os.listdir("docs")
    if doc_files:
        st.sidebar.subheader("Processing Status")
        st.sidebar.info(f"{len(doc_files)} document(s) ready for indexing")

        with st.spinner(f"Indexing {len(doc_files)} document(s)..."):
            try:
                # Logging file types
                file_types = ", ".join(set(os.path.splitext(f)[1] for f in doc_files))
                logger.info(f"File Types: {file_types}")

                # Loading & Indexing
                documents = SimpleDirectoryReader("docs").load_data()
                st.session_state.index = VectorStoreIndex.from_documents(documents)
                st.session_state_processed = True
                st.success("Document(s) Indexed Successfully")

            except Exception as e:
                st.error(f"Error in indexing document(s): {str(e)}")
                logger.exception("Indexing Error")
    else:
        st.info("Upload Document(s) in the Sidebar to get started")

# Query

if not(st.session_state.index and st.session_state.processed):
    st.divider()
    st.success("Ready for Questions!")
    query = st.text_input("Ask questions relating to the document(s):", placeholder = "Type your question here", key = "query_input")
    
    if query:
        with st.spinner("Searcing Document(s)..."):
            try:
                response = st.session_state.index.as_query_engine().query(query)
                st.subheader("Answer:")
                st.write(response.response)

                with st.expander("Source Document(s)"):
                    for i, node in enumerate(response.source_nodes):
                        st.markdown(f"** Document(s) {i+1}: ** '{node.metadata.get('file_name', 'Unknown')}")
                        st.caption(node.text[:500] + "..." if len(node.text) > 500 else node.text)
            except Exception as e:
                st.error(f"Error Generating Response: {str(e)}")