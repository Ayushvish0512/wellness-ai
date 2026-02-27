import os
from llama_cpp import Llama

# Get the absolute path to the directory where this file is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "smollm-360m-instruct-q4_k_m.gguf")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)

