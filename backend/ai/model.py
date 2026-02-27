import os
import urllib.request
from llama_cpp import Llama

# This is where your code is running
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📁 Where the model should live
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "smollm-360m-instruct-q4_k_m.gguf")

# 🌍 The Direct Download Link (Public)
URL = "https://huggingface.co/cakeisalie/SmolLM-360M-Instruct-GGUF/resolve/main/smollm-360m-instruct-q4_k_m.gguf"

# 🛠 1. Check if model exists locally
if not os.path.exists(MODEL_PATH):
    print(f"☁️ Model not found. Downloading from public mirror...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    try:
        # Download the file directly
        urllib.request.urlretrieve(URL, MODEL_PATH)
        print("✅ Download Complete!")
    except Exception as e:
        print(f"❌ Download Failed: {e}")
        raise e
else:
    print(f"✅ Using existing model at: {MODEL_PATH}")

# 🚀 2. Start the AI Engine
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)




