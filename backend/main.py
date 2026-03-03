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

#-------- CORS Middleware --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be False for wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Chat Endpoint --------
@app.post("/chat")
def chat(request: ChatRequest):
    print(f"📥 Received request from user: {request.user_id}")
    print(f"💬 Message: {request.message}")
    
    # 🔹 Step 1: Load conversation history from DB
    try:
        history = get_history(request.user_id)
        print(f"📚 Loaded history: {len(history)} messages")
    except Exception as e:
        print(f"❌ Error loading history: {e}")
        history = []

    # 🔹 Step 2: Check if user is asking for their last message
    last_message_keywords = [
        "what was my last message", "what did i just ask", 
        "repeat my last question", "what was my previous message",
        "last message", "last msg"
    ]
    
    if any(keyword in request.message.lower() for keyword in last_message_keywords):
        user_messages = [msg for msg in history if msg["role"] == "user"]
        if user_messages:
            ai_response = f"Your last message was: '{user_messages[-1]['content']}'"
        else:
            ai_response = "I don't see any previous messages from you in this session."
    else:
        # 🔹 Step 3: Generate AI response normally
        ai_response = generate_response(
            message=request.message,
            lifestyle_area=request.lifestyle_area,
            history=history
        )
    
    print(f"🤖 AI Response generated ({len(ai_response)} chars)")

    # 🔹 Step 4: Save current messages to DB
    save_message(request.user_id, "user", request.message)
    save_message(request.user_id, "assistant", ai_response)
    
    print(f"✅ Saved to DB. Sending response...")

    return {
        "user_id": request.user_id,
        "question": request.message,
        "response": ai_response,
        "status": "success"
    }
