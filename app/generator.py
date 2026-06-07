import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.prompts import SYSTEM_PROMPT

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
USE_GROQ = os.getenv("USE_GROQ", "true").lower() == "true"


class SegmentationBrief(BaseModel):
    business_objective: str = Field(description="The business goal behind the request")
    target_population: str = Field(description="Who the analysis is focused on")
    recommended_segmentation_approach: str = Field(description="The best-fit segmentation approach based on the provided context")
    alternative_approaches: List[str] = Field(description="Other reasonable approaches if applicable")
    suggested_variables: List[str] = Field(description="Useful variables or features to consider")
    recommended_method: str = Field(description="Rules-based, clustering-based, hybrid, etc.")
    expected_deliverables: List[str] = Field(description="Likely outputs for the stakeholder")
    assumptions_and_risks: List[str] = Field(description="Important assumptions, ambiguities, and risks")
    missing_information: List[str] = Field(description="Information needed to improve the recommendation")


def _get_model():
    if USE_GROQ:
        from langchain_groq import ChatGroq
        return ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
    else:
        from langchain_ollama import ChatOllama
        return ChatOllama(model="qwen2.5:3b", temperature=0)


def generate_brief(question: str, retrieved_context: str) -> SegmentationBrief:
    model = _get_model()
    structured_model = model.with_structured_output(SegmentationBrief)

    prompt = f"""
            {SYSTEM_PROMPT}

            User question:
            {question}

            Retrieved context:
            {retrieved_context}

            Generate a practical segmentation brief.
            """

    return structured_model.invoke(prompt)
