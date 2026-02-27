from fastapi import FastAPI
from pydantic import BaseModel
from backend.ai.generate import generate_response
from backend.db.chat_store import save_message, get_history
from fastapi.middleware.cors import CORSMiddleware

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

#-------- CORS Middleware --------for development (allow all origins, later restrict to frontend domain) --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
