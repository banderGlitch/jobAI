from google.adk.agents import Agent


from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

# Remote Scout Agent (A2A)
scout_agent = RemoteA2aAgent(
    name="source_scout_agent",
    description="Remote Scout Agent exposed via A2A",
    agent_card=(
        "http://localhost:8001"
        + AGENT_CARD_WELL_KNOWN_PATH
    ),
)

# Root Planner Agent (THIS MUST BE Agent, NOT BaseAgent)
planner_agent = Agent(
    name="planner_agent",
    description="Root planner agent that orchestrates job discovery",
    model="gemini-2.0-flash",
    sub_agents=[scout_agent],
    instructions="""
    You are a planner agent.
    Delegate job discovery to the source_scout_agent.
    Return the scout agent's response as structured data.
    """,
)
