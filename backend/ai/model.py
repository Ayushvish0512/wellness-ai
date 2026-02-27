import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# This is where your code is running
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Look for the model file you already have in backend/models/
LOCAL_FILENAME = "smollm-360m-instruct-q4_k_m.gguf"
LOCAL_PATH = os.path.join(BASE_DIR, "models", LOCAL_FILENAME)

if os.path.exists(LOCAL_PATH):
    print(f"✅ Found local model: {LOCAL_PATH}")
    MODEL_PATH = LOCAL_PATH
else:
    # 2. If it's NOT there (like on Render), download it automatically
    print("☁️ Model not found on server. Downloading from Hugging Face...")
    try:
        MODEL_PATH = hf_hub_download(
            repo_id="cakeisalie/SmolLM-360M-Instruct-GGUF",
            filename="smollm-360m-instruct-q4_k_m.gguf",
            local_dir=os.path.dirname(LOCAL_PATH)
        )
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        raise e

# 3. Load the model into the AI engine
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)



