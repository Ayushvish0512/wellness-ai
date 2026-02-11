from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

llm = Llama(
    model_path="models/smollm-360m-instruct-q4_k_m.gguf",
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)



# -------- Request Model --------
class ChatRequest(BaseModel):
    user_id: str
    message: str
    lifestyle_area: str | None = None


# -------- Root Endpoint --------
@app.get("/")
def home():
    return {"message": "Wellness AI Backend Running"}


# -------- Health Check --------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------- Chat Endpoint --------
@app.post("/chat")
def chat(request: ChatRequest):

    prompt = f"""
### Instruction:
You are a helpful wellness AI assistant.
Give short, practical wellness advice.

Lifestyle area: {request.lifestyle_area}
User message: {request.message}

### Response:
"""

    output = llm(
        prompt,
        max_tokens=150,
        temperature=0.7
    )

    ai_response = output["choices"][0]["text"].strip()

    return {
        "user_id": request.user_id,
        "question": request.message,
        "response": ai_response,
        "status": "success"
    }
