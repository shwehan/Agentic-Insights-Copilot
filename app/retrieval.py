from pathlib import Path

from langchain_core.documents import Document
# from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# load segmentation_playbook.md
DATA_PATH = Path("data/segmentation_playbook.md")
CHROMA_DIR = "chroma_store" # for later storing the chunked/embedded segmentation playbook in here
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# load 
def load_source_text() -> str:
    return DATA_PATH.read_text(encoding="utf-8")

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# chunking & embedding 
def build_vectorstore():
    text = load_source_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
    )
    docs = splitter.split_documents(
        [Document(page_content=text, metadata={"source": str(DATA_PATH)})]
    )

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="segmentation_playbook",
    )
    return vectorstore

_retriever_cache = None


def _build_retriever():
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_name="segmentation_playbook",
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def get_retriever():
    global _retriever_cache
    if _retriever_cache is None:
        _retriever_cache = _build_retriever()
    return _retriever_cache


if __name__ == "__main__":
    build_vectorstore()
    print("Vector store built successfully.")