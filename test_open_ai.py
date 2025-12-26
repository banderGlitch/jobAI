from job_intelligence_agents.llm.executor import run_llm

print(run_llm("Reply with OK"))


# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from openai import OpenAI

# # --- Load .env FIRST ---
# env_path = Path(__file__).parent / "job_intelligence_agents" / "planner_agent" / ".env"
# load_dotenv(env_path)

# # --- DEBUG (do NOT skip) ---
# print("ENV PATH EXISTS:", env_path.exists())
# print("OPEN_AI_API_KEY:", os.getenv("OPEN_AI_API_KEY"))

# # --- FAIL FAST ---
# if not os.getenv("OPEN_AI_API_KEY"):
#     raise RuntimeError("OPEN_AI_API_KEY is NOT loaded")

# # --- Create client ---
# client = OpenAI(
#     api_key=os.getenv("OPEN_AI_API_KEY")
# )

# resp = client.responses.create(
#     model="gpt-4o-mini",
#     input="Reply with OK"
# )

# print(resp.output_text)
