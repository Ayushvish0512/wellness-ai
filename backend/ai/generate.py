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

    # -------- Build the prompt in Llama format --------
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"<|system|>\n{msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"<|user|>\n{msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"<|assistant|>\n{msg['content']}\n"
    
    prompt += "<|assistant|>\n"

    # -------- Generate Response --------
    output = llm(
        prompt,
        max_new_tokens=150,
        temperature=0.7,
        stop=["<|user|>", "<|system|>"]
    )

    # Extract the generated text
    generated_text = output.strip()
    
    # Remove the prompt from the response if it appears
    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):].strip()
    
    return generated_text
