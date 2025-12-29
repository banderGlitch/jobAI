import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Scout Agent using OpenAI (via LiteLLM)
scout_agent = LlmAgent(
    name="source_scout_agent",
    description="Discovers fresh job posting URLs based on role, experience, and location",
    model=LiteLlm(
        "gpt-4o-mini",  # Using mini for cost efficiency
        api_key=os.environ.get("OPEN_AI_API_KEY")
    ),
    instruction="""You are a Source Scout Agent specialized in finding job posting URLs.

YOUR TASK:
- Given a job search query, identify and return real job board URLs and company career page URLs
- Return ONLY structured metadata about job sources (URLs, source names)
- DO NOT generate fake URLs or invent job postings

OUTPUT FORMAT (JSON):
{
    "sources": [
        {
            "url": "https://www.indeed.com/jobs?q=java+developer&l=san+francisco",
            "source_name": "Indeed",
            "source_type": "job_board"
        },
        {
            "url": "https://www.linkedin.com/jobs/search/?keywords=java%20developer&location=San%20Francisco",
            "source_name": "LinkedIn Jobs",
            "source_type": "job_board"
        }
    ],
    "search_summary": "Found 2 job boards for Java Developer in San Francisco"
}

RULES:
- Use real, well-known job boards (Indeed, LinkedIn, Glassdoor, Wellfound, etc.)
- Construct proper search URLs with query parameters
- Keep responses concise and structured
- NO hallucinated job listings, ONLY source URLs"""
)

# REQUIRED: root_agent symbol
root_agent = scout_agent

# REQUIRED: expose via A2A (auto-generates agent card)
a2a_app = to_a2a(root_agent, port=8001)
