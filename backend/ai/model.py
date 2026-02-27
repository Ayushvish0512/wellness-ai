import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Base directory for the backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define model details (using a verified public repo)
REPO_ID = "bartowski/SmolLM-360M-Instruct-GGUF"
FILENAME = "SmolLM-360M-Instruct-Q4_K_M.gguf"
OLD_FILENAME = "smollm-360m-instruct-q4_k_m.gguf"

# Local path inside the project
LOCAL_MODEL_PATH = os.path.join(BASE_DIR, "models", FILENAME)
OLD_LOCAL_PATH = os.path.join(BASE_DIR, "models", OLD_FILENAME)

# Check if model exists locally (new or old name), otherwise download it
if os.path.exists(LOCAL_MODEL_PATH):
    MODEL_PATH = LOCAL_MODEL_PATH
elif os.path.exists(OLD_LOCAL_PATH):
    MODEL_PATH = OLD_LOCAL_PATH
else:
    print(f"Model not found. Downloading {FILENAME} from Hugging Face...")
    os.makedirs(os.path.dirname(LOCAL_MODEL_PATH), exist_ok=True)
    MODEL_PATH = hf_hub_download(
        repo_id=REPO_ID, 
        filename=FILENAME, 
        local_dir=os.path.dirname(LOCAL_MODEL_PATH)
    )


print(f"Loading model from: {MODEL_PATH}")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)


