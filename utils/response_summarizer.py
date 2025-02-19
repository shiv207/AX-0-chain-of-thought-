import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("api-key")
if not api_key:
    raise ValueError("API key not found in .env file")
genai.configure(api_key=api_key)

def summarize_response(final_response):
    """
    Takes the final response and returns a user-friendly summary using Gemini.
    """
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-002'
    )
    
    prompt = f"""
    Please provide a simple, clear summary of the following technical response. 
    Focus on the main findings and explain them in a way that a non-technical person would understand:
    when returning code, return the complete code in a code block, returned by the agent.

    {final_response}
    
    Keep your response concise and friendly. Avoid technical jargon where possible.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else "Sorry, I couldn't generate a summary."
    except Exception as e:
        return f"Error generating summary: {str(e)}" 