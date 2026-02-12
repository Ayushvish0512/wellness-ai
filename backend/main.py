'''from fastapi import FastAPI
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
    }'''


from fastapi import FastAPI
from pydantic import BaseModel
from ai.generate import generate_response
from db.chat_store import save_message, get_history

app = FastAPI()

# -------- Request Model --------
class ChatRequest(BaseModel):
    user_id: str
    message: str
    lifestyle_area: str | None = None
    history: list[dict] | None = None   

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
    # 🔹 Step 1: Load conversation history from DB
    history = get_history(request.user_id)
    print("LOADED HISTORY:", history)

    # 🔹 Step 2: Check if user is asking for their last message
    last_message_keywords = [
        "last message", "last msg", "last question", "what was my last message",
        "what's my last question", "whats my last msg"
    ]

    asking_last_message = any(k in request.message.lower() for k in last_message_keywords)

    last_user_message = None
    if asking_last_message:
        # Exclude the current message (ask about last) from search
        for msg in reversed(history):
            if msg["role"] == "user" and msg["content"].strip().lower() != request.message.strip().lower():
                last_user_message = msg["content"]
                break

        ai_response = (
            f"Your last message was: '{last_user_message}'"
            if last_user_message else
            "You have no previous messages."
        )
    else:
        # 🔹 Step 3: Generate AI response normally
        ai_response = generate_response(
            message=request.message,
            lifestyle_area=request.lifestyle_area,
            history=history
        )

    # 🔹 Step 4: Save current messages to DB
    save_message(request.user_id, "user", request.message)
    save_message(request.user_id, "assistant", ai_response)

    return {
        "user_id": request.user_id,
        "question": request.message,
        "response": ai_response,
        "status": "success"
    }