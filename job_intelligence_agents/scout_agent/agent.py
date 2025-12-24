from google.adk.agents.base_agent import BaseAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

class SourceScoutAgent(BaseAgent):
    def run(self, input: dict) -> dict:
        return {
            "criteria": input,
            "job_sources": [
                {
                    "url": "https://careers.example.com/java-dev",
                    "source": "company-careers",
                    "discovered_at": "2025-01-01T10:00:00Z"
                }
            ]
        }

scout_agent = SourceScoutAgent(
    name="source_scout_agent",
    description="Discovers fresh job posting URLs"
)

a2a_app = to_a2a(scout_agent, port=8001)
