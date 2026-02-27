from backend.ai.model import llm
from typing import List, Dict, Optional

def generate_response(
    message: str,
    lifestyle_area: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
):
    # -------- System Behavior Control --------
    system_prompt = f"""
You are a professional wellness coach.

You have access to the full conversation history.

Important:
- If the user asks about their previous message or question,
  look only at previous USER messages (ignore assistant replies).
- Answer accurately using the conversation history.

Rules:
- Give practical, safe advice.
- Never provide medical diagnosis.
- Keep responses under 120 words.
- Tone: calm, supportive.

Lifestyle focus: {lifestyle_area or "general wellness"}
"""

    # -------- Build Chat Messages --------
    messages = [
        {
            "role": "system",
            "content": system_prompt.strip()
        }
    ]

    # -------- Add Conversation History (if any) --------
    if history:
        messages.extend(history)

    # -------- Add Current User Message --------
    messages.append({
        "role": "user",
        "content": message
    })

    # -------- Generate Response --------
    output = llm.create_chat_completion(
        messages=messages,
        max_tokens=150,
        temperature=0.7,
    )

    return output["choices"][0]["message"]["content"].strip()
