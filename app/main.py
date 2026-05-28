# KB Assistant v2 — Azure OpenAI + Terraform + GitHub Actions + Docker

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

from ingest import load_docs_from_blob, chunk_docs
from retrieval import get_top_chunks
from openai_client import ask_question

app = FastAPI(title="KB Assistant")

# Load and chunk docs once at startup
chunks = []

@app.on_event("startup")
async def startup_event():
    global chunks
    storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME", "")
    if storage_account_name:
        container_url = f"https://{storage_account_name}.blob.core.windows.net"
        docs = load_docs_from_blob(container_url)
        chunks = chunk_docs(docs)
        print(f"Loaded {len(chunks)} chunks from {len(docs)} documents")
    else:
        print("No storage account configured — running without docs")

class QuestionRequest(BaseModel):
    question: str
    password: str

class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]

APP_PASSWORD = os.environ.get("APP_PASSWORD", "changeme")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>KB Assistant</title></head>
        <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>KB Assistant</h1>
            <div>
                <input type="password" id="password" placeholder="Password" 
                       style="width: 100%; padding: 10px; margin: 10px 0;">
                <textarea id="question" placeholder="Ask a question..." 
                          style="width: 100%; height: 100px; padding: 10px; margin: 10px 0;"></textarea>
                <button onclick="askQuestion()" 
                        style="padding: 10px 20px; background: #0078d4; color: white; border: none; cursor: pointer;">
                    Ask
                </button>
                <div id="answer" style="margin-top: 20px; padding: 15px; background: #f5f5f5;"></div>
            </div>
            <script>
                async function askQuestion() {
                    const question = document.getElementById('question').value;
                    const password = document.getElementById('password').value;
                    const answerDiv = document.getElementById('answer');
                    answerDiv.innerHTML = 'Thinking...';
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({question, password})
                    });
                    const data = await response.json();
                    if (response.ok) {
                        answerDiv.innerHTML = '<strong>Answer:</strong><br>' + data.answer + 
                            '<br><br><small>Sources: ' + data.sources.join(', ') + '</small>';
                    } else {
                        answerDiv.innerHTML = 'Error: ' + data.detail;
                    }
                }
            </script>
        </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "healthy", "chunks_loaded": len(chunks)}

@app.post("/ask", response_model=QuestionResponse)
async def ask(request: QuestionRequest):
    if request.password != APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if not chunks:
        raise HTTPException(status_code=503, detail="No documents loaded")

    top_chunks = get_top_chunks(chunks, request.question)
    answer = ask_question(request.question, top_chunks)
    sources = list(set([chunk["source"] for chunk in top_chunks]))

    return QuestionResponse(answer=answer, sources=sources)