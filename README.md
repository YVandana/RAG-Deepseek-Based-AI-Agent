# 📃💬DeepSeek RAG Agent

<img width="1920" height="998" alt="Example-0" src="https://github.com/user-attachments/assets/14c5a3b6-ac30-4eab-9bd6-78477946ee64" />

A local RAG system using Ollama (Deepseek) and Hugging Face embeddings for document Q&A and interaction.


https://github.com/user-attachments/assets/f866f3ac-8eb0-404b-b671-0a930d646fcf


## Features
- Upload documents of various types (PDF, TXT, MD, DOCX & PPTX)
- Ask questions about your documents
- View sources and excerpts
- Runs entirely locally

## ✔️Requirements
1. [Ollama](https://ollama.com/) installed
2. Python 3.8+
3. Requires ~4GB RAM for DeepSeek model
4. Uses `BAAI/bge-small-en-v1.5` embeddings (local)

### ⚙️Packages
1. streamlit>=1.33.0
2. llama-index-core>=0.10.34
3. llama-index-llms-ollama>=0.1.6
4. llama-index-embeddings-huggingface>=0.1.4
5. python-dotenv>=1.0.0

## ⌨️Setup

### 1. Install Ollama & pull model
```bash
ollama pull deepseek-llm
ollama serve # If Ollama is not running use
```
### 2. Create virtual environment (New Terminal)
```bash
python -m venv rag_env
```
```bash
source rag_env/bin/activate  # Linux/Mac
rag_env\Scripts\activate   # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 👩‍💻⌨Usage
To run the
```bash
streamlit run rag_agent.py
```
**Upload documents through the UI and ask questions!**

**Note!**
Documents are stored locally in `docs/`

## Example Usage
1. Example of uploading a .txt file to be indexed and processed

https://github.com/user-attachments/assets/5eb80ad5-fc51-4d16-b5eb-293b91c86349

2. Example when used a .txt file with the query 'Can youi give me a summary'
<img width="1920" height="998" alt="Example-2" src="https://github.com/user-attachments/assets/63a427fb-2df0-434e-b30b-ca17fd6a81ef" />

