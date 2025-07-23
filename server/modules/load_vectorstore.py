import os
from pathlib import Path
from langchain.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

PERSIST_DIR="./chroma_store"
UPLOAD_DIR="./uploaded_pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

def load_vectorstore(uploaded_files):
    file_path=[]

    for file in uploaded_files:
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path,"wb") as f:
            f.write(file.file.read())
        file_path.append(str(save_path))    
    
    docs=[]
    for path in file_path:
        loader=PyPDFLoader(path)
        docs.extend(loader.load())

    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    texts=splitter.split_documents(docs)

    embedding_model=SentenceTransformer(model_name="all-MiniLM-L12-v2")

    if(os.path.exists(PERSIST_DIR)) and os.listdir(PERSIST_DIR):
        vectorstore=Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model
        )
        vectorstore.add_documents(texts)
        vectorstore.persist()
    else:
        vectorstore=Chroma.from_documents(
            documents=texts,
            embedding=embedding_model,
            persist_directory=PERSIST_DIR
        )
        vectorstore.persist()
        return vectorstore