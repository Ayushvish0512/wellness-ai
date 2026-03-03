import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# This is where your code is running
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📁 Where the model should live
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "SmolLM2-360M-Instruct-Q4_K_M.gguf")

# 🌍 The Direct Download Link (Public SmolLM2)
URL = "https://huggingface.co/bartowski/SmolLM2-360M-Instruct-GGUF/resolve/main/SmolLM2-360M-Instruct-Q4_K_M.gguf?download=true"

# 🛠 1. Check if model exists locally
if not os.path.exists(MODEL_PATH):
    print(f"☁️ Model not found. Downloading SmolLM2 from public mirror...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    try:
        # We add a User-Agent because some servers block basic urllib requests with a 401
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(MODEL_PATH, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print("✅ Download Complete!")
    except Exception as e:
        print(f"❌ Download Failed: {e}")
        # If it fails, we try a secondary mirror or just fail gracefully
        raise e
else:
    print(f"✅ Using existing model at: {MODEL_PATH}")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)








