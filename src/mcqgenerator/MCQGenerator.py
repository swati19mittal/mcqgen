import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .utils import extract_json_from_response
from .logger import get_logger

load_dotenv()
logger = get_logger("MCQGenerator")

DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
TOGETHER_BASE = "https://api.together.xyz/v1"

TEMPLATE = """
You are an expert content writer that converts a passage into well-structured multiple-choice questions (MCQs).

Instructions:
- Generate exactly {number} MCQs based on the passage below.
- For each question generate 4 options labeled A, B, C, D.
- Clearly mark which option is the correct answer.
- Keep questions concise and unambiguous.
- Output must be a JSON object like:
{{ 
  "source_summary": "<one-line summary>",
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "answer": "A"
    }},
    ...
  ]
}}

Passage:
{text}
"""

class MCQGenerator:
    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0.0):
        key = os.getenv("TOGETHER_API_KEY")
        if not key:
            raise ValueError("Set TOGETHER_API_KEY in .env")
        # point ChatOpenAI to Together's base URL
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=key,
            openai_api_base=TOGETHER_BASE,
            temperature=temperature
        )

        self.prompt = PromptTemplate(
            input_variables=["text", "number"],
            template=TEMPLATE
        )

    def generate(self, text: str, number: int = 5):
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        logger.info("Sending prompt to LLM (Together.ai)")
        out = chain.run({"text": text, "number": number})
        logger.info("LLM returned text; attempting to extract JSON")
        try:
            parsed = extract_json_from_response(out)
            return parsed
        except Exception as e:
            logger.error("Failed to parse JSON from LLM output: %s", e)
            # return raw text as fallback
            return {"raw": out}

