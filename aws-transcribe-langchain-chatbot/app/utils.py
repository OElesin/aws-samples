from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

INDEX_PATH = './embeddings'
hf_embeddings = HuggingFaceEmbeddings()

def load_faiss_index():
    """
    Load saved FAISS embeddings
    """
    return FAISS.load(INDEX_PATH, hf_embeddings)