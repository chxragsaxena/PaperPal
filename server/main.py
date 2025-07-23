from fastapi import FastAPI,UploadFile,File,Form,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.llm import get_llm_chain
from modules.load_vectorstore import load_vectorstore
from modules.query_handle import query_chain
from langchain.chains import RetrievalQA
from log import logger


app= FastAPI(title="JioGPT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        logger.exception("Unhandled exception occurred")
        return JSONResponse(
            status_code=500,
            content={"error":str(ex)}
        )
@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"received {len(files)} files")
        load_vectorstore(files)
        logger.info("documents added to Chroma")
        return {"message": "Files processed and vectorstore updated successfully"}
    except Exception as e:
        logger.exception("Error uploading pdf")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask/")
async def ask_question(question:str=Form(...)):
    try:
        logger.info(f"user query:{question}")
        from langchain_community.vectorstores import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        from modules.load_vectorstore import PERSIST_DIR

        vectorstore=Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
        )
        chain=get_llm_chain(vectorstore)
        result=query_chain(chain,question)
        logger.info("query successful")
        return result
    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500,content={"error":str(e)})
    



@app.get("/test")
async def test():
    return {"measage": "Hello, JioGPT!"}