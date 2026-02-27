import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Base directory for the backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define model details
REPO_ID = "HuggingFaceTB/SmolLM-360M-Instruct-GGUF"
FILENAME = "smollm-360m-instruct-q4_k_m.gguf"

# Local path inside the project
LOCAL_MODEL_PATH = os.path.join(BASE_DIR, "models", FILENAME)

# Check if model exists locally, otherwise download it
if not os.path.exists(LOCAL_MODEL_PATH):
    print(f"Model not found at {LOCAL_MODEL_PATH}. Downloading from Hugging Face...")
    os.makedirs(os.path.dirname(LOCAL_MODEL_PATH), exist_ok=True)
    # This downloads to the Hub cache and returns the path, but we can also download directly to our folder
    MODEL_PATH = hf_hub_download(repo_id=REPO_ID, filename=FILENAME, local_dir=os.path.dirname(LOCAL_MODEL_PATH))
else:
    MODEL_PATH = LOCAL_MODEL_PATH

print(f"Loading model from: {MODEL_PATH}")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)


