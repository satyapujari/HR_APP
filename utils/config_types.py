from enum import Enum

class LLMType(str, Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"

class EmbeddingModelType(str, Enum):
    OPENAI = "openai"
    OPENAI_LARGE = "openai-large"
    HUGGINGFACE = "huggingface"

class VectorDBType(str, Enum):
    FAISS = "faiss"
    PINECONE = "pinecone"
    MILVUS = "milvus"
    CHROMA = "chroma"