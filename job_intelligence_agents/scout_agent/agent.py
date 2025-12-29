import os
import requests
from dotenv import load_dotenv
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.function_tool import FunctionTool

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


def search_jobs(role: str, location: str = "") -> str:
    """
    Search for actual job listings using Adzuna API.
    
    Args:
        role: Job title or role (e.g., "Java Developer", "Data Scientist")
        location: Location (e.g., "San Francisco", "Remote", "NYC")
    
    Returns:
        Formatted job listings with titles, companies, and URLs
    """
    # Adzuna API configuration
    app_id = os.environ.get("ADZUNA_APP_ID", "demo")  # Get your free key at https://developer.adzuna.com/
    app_key = os.environ.get("ADZUNA_APP_KEY", "demo")
    
    # Build API request
    country = "us"  # Can be made dynamic
    what = role.replace(" ", "+")
    where = location.replace(" ", "+") if location else ""
    
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 10,
        "what": what,
        "where": where
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        
        if not results:
            return f"No jobs found for '{role}' in '{location}'. Try different criteria."
        
        # Format results
        output = f"🎯 FOUND {len(results)} JOB LISTINGS\n\n"
        output += f"Search: {role}" + (f" in {location}" if location else "") + "\n"
        output += "─" * 50 + "\n\n"
        
        for i, job in enumerate(results[:5], 1):  # Show top 5
            title = job.get("title", "N/A")
            company = job.get("company", {}).get("display_name", "N/A")
            location_str = job.get("location", {}).get("display_name", "N/A")
            url = job.get("redirect_url", "#")
            salary = job.get("salary_max", None)
            
            output += f"#{i} {title}\n"
            output += f"   🏢 {company}\n"
            output += f"   📍 {location_str}\n"
            if salary:
                output += f"   💰 Up to ${salary:,.0f}/year\n"
            output += f"   🔗 {url}\n\n"
        
        output += "─" * 50 + "\n"
        output += f"💡 Showing top {min(5, len(results))} of {len(results)} results"
        
        return output
        
    except Exception as e:
        return f"Error fetching jobs: {str(e)}. Using fallback job boards instead."


# Scout Agent using OpenAI with job search tool
scout_agent = LlmAgent(
    name="source_scout_agent",
    description="Discovers real job listings using API",
    model=LiteLlm(
        "gpt-4o-mini",
        api_key=os.environ.get("OPEN_AI_API_KEY")
    ),
    tools=[FunctionTool(search_jobs)],
    instruction="""You are a Source Scout Agent that finds REAL job listings.

TASK:
1. Extract role and location and experience from user query 
2. Call the 'search_jobs' function to fetch actual job postings
3. Return the results

EXAMPLES:
- "Find Java jobs in SF" → search_jobs(role="Java Developer", location="San Francisco")
- "Python developer remote" → search_jobs(role="Python Developer", location="Remote")
- "Find jobs" (vague) → Ask: "What role are you interested in?"

RULES:
- Always use the search_jobs tool for job queries
- If query is too vague, ask for role/location
- Format output cleanly"""
)

# REQUIRED: root_agent symbol
root_agent = scout_agent

# REQUIRED: expose via A2A
a2a_app = to_a2a(root_agent, port=8001)
