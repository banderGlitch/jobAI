from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm



from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

# Remote Scout Agent (A2A)
scout_agent = RemoteA2aAgent(
    name="source_scout_agent",
    description="Remote Scout Agent exposed via A2A",
    agent_card=(
        "http://localhost:8001"+ AGENT_CARD_WELL_KNOWN_PATH
    ),
)


import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from specific .env file location


env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Planner Agent using OpenAI (via LiteLLM)
planner_agent = LlmAgent(
    name="planner_agent",
    description="Root planner agent (OpenAI-powered)",
    model=LiteLlm(
        "gpt-4o",  # Positional argument for model name
        api_key=os.environ.get("OPEN_AI_API_KEY") # Ensure this is set in .env
    ),
    # instructions="""
    # You are a Job Planner Agent.
    # Your goal is to help users find jobs by orchestrating other agents.
    
    # When a user asks for jobs:
    # 1. Call the 'source_scout_agent' to find job sources.
    # 2. Summarize the findings for the user.
    # """,
    sub_agents=[scout_agent]
)

# Note: LlmAgent handles the "run" logic automatically using the LLM 
# and the tools/sub-agents provided.

# The ADK runner looks for a variable named 'root_agent' by default
root_agent = planner_agent
