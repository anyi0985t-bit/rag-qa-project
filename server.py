from fastapi import FastAPI, HTTPException
from docs import documents
from rag_bot import ask_ollama, search_final

app = FastAPI()

@app.post("/chat")
def chat(question: str):
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    found_docs = search_final(question, documents, k=2)
    context = "\n".join(found_docs)
    answer = ask_ollama(question, context)
    return {"answer": answer, "sources": found_docs}