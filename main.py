# main.py

import logging
import os
import time
from dotenv import load_dotenv
import re

from agents.agent_factory import AgentFactory
from utils.user_input_handler import get_user_input
from utils.result_formatter import format_results
from utils.response_summarizer import summarize_response

import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Ensure logs directory exists
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='logs/system.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure the Gemini API
api_key = os.getenv("api-key")
if not api_key:
    raise ValueError("API key not found in .env file")
    
genai.configure(api_key=api_key)

def main():
    # Step 1: User Input Handler
    user_problem = get_user_input()
    logger.info("User problem received: %s", user_problem)

    # Step 2: Sequential Processing through Agents
    agent_factory = AgentFactory()
    agents = agent_factory.create_agents()  # Returns the list of agents in sequence

    previous_solution = None
    all_solutions = []

    for agent in agents:
        solution = agent.get_solution(user_problem, previous_solution)
        all_solutions.append((agent.name, solution))
        previous_solution = solution  # Pass the current solution to the next agent

    # Step 3: Final Output
    final_solution = previous_solution

    # Step 4: Result Formatting and Output
    formatted_result = format_results(all_solutions, final_solution)
    
    # Step 5: Generate user-friendly summary
    user_friendly_summary = summarize_response(final_solution)
    
    print("\n=== Simple Summary ===")
    print(user_friendly_summary)
    
    # If the user's problem asks for a program, display the code blocks from the final solution
    code_blocks = re.findall(r"```python[\s\S]*?```", final_solution)
    if code_blocks:
        print("\n=== Complete Finished Code ===")
        for block in code_blocks:
            print(block)
    
    print("\n=== Technical Details ===")
    print("Final Answer:")
    print(final_solution)
    print("\nDetailed Reasoning and Steps:")
    print(formatted_result)

if __name__ == "__main__":
    main()
