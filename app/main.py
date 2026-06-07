from dotenv import load_dotenv

from app.retrieval import build_vectorstore, get_retriever
from app.generator import generate_brief, SegmentationBrief

load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def run_pipeline(question: str) -> SegmentationBrief:
    retriever = get_retriever()
    docs = retriever.invoke(question)
    context = format_docs(docs)
    return generate_brief(question, context)


if __name__ == "__main__":
    while True:
        question = input("Enter a business question (or 'quit' to exit): ").strip()
        if question.lower() == "quit":
            break
        if not question:
            continue
        brief = run_pipeline(question)
        print(brief.model_dump_json(indent=2))
