from google.adk.agents.base_agent import BaseAgent as Agent

from google.adk.a2a.utils.agent_to_a2a import to_a2a


#-----------------------
#    Scout Agent
#-----------------------
class SourceScoutAgent(Agent):
    """
    Source Scout Agent
    - Discovers job posting URLs
    - Returns structured source metadata only
    """

    def run(self, input: dict) -> dict:

        role = input.get("role")
        experience = input.get("experience")
        location = input.get("location")

         # Phase-1: Deterministic static output
        # (This avoids hallucinations and keeps architecture clean)
        jobs = [
            {
                "url": "https://careers.example.com/java-developer-123",
                "source": "company-careers",
                "discovered_at": "2025-01-01T10:00:00Z"
            },
            {
                "url": "https://jobs.example.com/backend-java-456",
                "source": "job-board",
                "discovered_at": "2025-01-01T11:00:00Z"
            }
        ]


        return {
           "criteria": {
                "role": role,
                "experience": experience,
                "location": location
            },
            "job_sources": jobs
        }
    # IMPORTANT:
    # Agent name MUST be a valid Python identifier

scout_agent = SourceScoutAgent(
    name="source_scout_agent",
    description="Discovers fresh job posting URLs based on role, experience, and location."
)

# Expose agent via A2A
a2a_app = to_a2a(scout_agent)
