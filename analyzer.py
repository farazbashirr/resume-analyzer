from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
import time
from google.genai import errors

load_dotenv()
client = genai.Client()

MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = (
    "You are an expert technical recruiter and resume coach. "
    "Compare the resume against the job description honestly. "
    "Only list skills as matched if the resume actually shows them. "
    "Keep every item short and specific."
)


class Analysis(BaseModel):
    match_score: int
    summary: str
    skills_matched: list[str]
    skills_missing: list[str]
    experience_gaps: list[str]
    recommended_improvements: list[str]


def analyze_resume(resume_text, job_description):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=Analysis,
                ),
            )
            return response.parsed.model_dump()
        except errors.ServerError:
            if attempt == 2:
                return None
            time.sleep(3 * (attempt + 1))