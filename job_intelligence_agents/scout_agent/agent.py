from typing import AsyncGenerator
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events.event import Event
from google.genai import types


class SourceScoutAgent(Agent):
    # Pydantic requires type annotations when overriding fields from base class
    name: str = "source_scout_agent"
    description: str = "Finds job sources"

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:

        """
        ADK-compliant implementation.
        Takes InvocationContext, yields Event objects.
        """
        # Extract input text from the last user message
        last_event = ctx.session.events[-1] if ctx.session.events else None
        input_text = ""
        if last_event and last_event.content and last_event.content.parts:
            for part in last_event.content.parts:
                if part.text:
                    input_text += part.text

        # Mock job sources (Phase 1: deterministic)

        jobs = [
            {"url": "https://careers.example.com/java-dev", "source": "company-careers"},
            {"url": "https://jobs.example.com/backend-java", "source": "job-board"}
        ]
        
        response_text = f"✅ Scout Agent successfully called!\n\nQuery: '{input_text}'\n\nFound sources:\n{jobs}"

        # Yield Event (required pattern)
        yield Event(
            author=self.name,
            content=types.Content(
                role="model",
                parts=[types.Part(text=response_text)]
            ),
            invocation_id=ctx.invocation_id,
            branch=ctx.branch
        )


# REQUIRED: root_agent symbol
root_agent = SourceScoutAgent()

# REQUIRED: expose via A2A (auto-generates agent card)
a2a_app = to_a2a(root_agent, port=8002)


# from google.adk.agents import Agent

# class SourceScoutAgent(Agent):
#     name = "source_scout_agent"
#     description = "Finds job sources"

#     async def _run_async_impl(self, input, context):
#         query = input.get("query", "")

#         return {
#             "agent": "source_scout_agent",
#             "called": True,
#             "query_received": query,
#             "results": [
#                 "Indeed",
#                 "LinkedIn",
#                 "Wellfound"
#             ]
#         }

# # 🔴 THIS IS THE CRITICAL LINE YOU ARE MISSING
# root_agent = SourceScoutAgent()






# from google.adk.agents import Agent
# from google.adk.a2a.server import A2AServer

# class SourceScoutAgent(Agent):
#     name = "source_scout_agent"
#     description = "Finds job sources"

#     async def _run_async_impl(self, input, context):
#         query = input.get("query", "")

#         return {
#             "agent": "source_scout_agent",
#             "called": True,
#             "query_received": query,
#             "results": [
#                 "Indeed",
#                 "LinkedIn",
#                 "Wellfound"
#             ]
#         }

# # 🔥 THIS is what uvicorn needs
# a2a_app = A2AServer(
#     agent=SourceScoutAgent()
# ).app


# from google.adk.agents.base_agent import BaseAgent
# from google.adk.a2a.utils.agent_to_a2a import to_a2a

# class SourceScoutAgent(BaseAgent):
#     def run(self, input: dict) -> dict:
#         return {
            
#             "criteria": input,
#             "job_sources": [
#                 {
#                     "url": "https://careers.example.com/java-dev",
#                     "source": "company-careers",
#                     "discovered_at": "2025-01-01T10:00:00Z"
#                 }
#             ]
#         }

# scout_agent = SourceScoutAgent(
#     name="source_scout_agent",
#     description="Discovers fresh job posting URLs"
# )

# a2a_app = to_a2a(scout_agent, port=8001)

