from llama_cpp import Llama

MODEL_PATH = "models/smollm-360m-instruct-q4_k_m.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    n_batch=128
)
