# agents/agent.py

import logging
import google.generativeai as genai
import re
import json

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, name, role_prompt):
        self.name = name
        self.role_prompt = role_prompt

    def get_solution(self, problem, previous_solution=None):
        messages = []

        # System prompt
        messages.append({"role": "system", "content": self.role_prompt})

        # User prompt
        if previous_solution:
            messages.append({"role": "user", "content": f"Problem:\n{problem}\n\nPrevious Solution:\n{previous_solution}\n\nPlease proceed with your analysis."})
        else:
            messages.append({"role": "user", "content": f"Problem:\n{problem}\n\nPlease provide your solution."})

        # Assistant initial acknowledgment
        messages.append({"role": "assistant", "content": "Understood. I will begin my reasoning steps now."})

        steps = []
        step_count = 1

        while True:
            # Build the prompt for the current reasoning step
            prompt = self.build_prompt(messages)

            response_text = self.make_api_call(prompt)

            if not response_text:
                logger.error(f"{self.name} did not return a valid response.")
                break  # Exit the loop if no response

            step_data = self.parse_response(response_text)

            if not step_data:
                logger.error(f"{self.name} failed to parse response: {response_text}")
                break  # Exit the loop on parsing failure

            # Log the response for debugging
            logger.info(f"{self.name} received response: {response_text}")
            logger.info(f"Parsed step data: {step_data}")

            # Store the step and content
            steps.append((f"Step {step_count}: {step_data['title']}", step_data['content']))

            messages.append({"role": "assistant", "content": response_text})

            if step_data['next_action'] == 'final_answer':
                break

            step_count += 1

        # Compile the agent's solution
        agent_solution = self.compile_solution(steps)
        logger.info(f"{self.name} completed their solution with steps: {steps}")
        return agent_solution

    def build_prompt(self, messages):
        # Combine messages into a single prompt
        prompt = ''
        for message in messages:
            role = message['role']
            content = message['content']
            if role == 'system':
                prompt += f"System: {content}\n\n"
            elif role == 'user':
                prompt += f"User: {content}\n\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n\n"
        return prompt

    def make_api_call(self, prompt):
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-001',
            tools='code_execution'
        )
        try:
            response = model.generate_content(prompt)
            return response.text if hasattr(response, 'text') else ""
        except Exception as e:
            logger.error(f"Error during API call for {self.name}: {str(e)}")
            return ""

    def parse_response(self, response_text):
        if not isinstance(response_text, str):
            logger.error(f"{self.name} received a non-string response: {response_text}")
            return None

        try:
            # First try to find JSON within code blocks
            json_pattern = r"```(?:json)?\s*(\{[\s\S]*?\})\s*```"
            match = re.search(json_pattern, response_text)
            if match:
                response_json = match.group(1)
                parsed_json = json.loads(response_json)
                
                # If there's a code block in the content, preserve it
                code_pattern = r"```(?:python)?\s*([\s\S]*?)```"
                code_match = re.search(code_pattern, parsed_json.get('content', ''))
                if code_match:
                    code_content = code_match.group(1)
                    parsed_json['code_block'] = code_content
                
                return parsed_json
            else:
                # Try to parse the entire response as JSON
                return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"{self.name} error parsing JSON response: {str(e)} - Response Text: {response_text}")
            return None

    def compile_solution(self, steps):
        solution_text = ""
        code_blocks = []
        
        # First pass: collect all code blocks and build regular content
        for title, content in steps:
            solution_text += f"### {title}\n{content}\n\n"
            
            # Extract any code blocks from the content
            code_pattern = r"```(?:python)?\s*([\s\S]*?)```"
            matches = re.finditer(code_pattern, content)
            for match in matches:
                code_blocks.append(match.group(1))

        # If this is Agent4 (final reviewer) and we have code blocks, add them to the final solution
        if self.name == "Agent4" and code_blocks:
            solution_text += "\n=== Complete Code ===\n"
            solution_text += "```python\n"
            # Join all code blocks, removing duplicate imports and constants
            unique_code = self.merge_code_blocks(code_blocks)
            solution_text += unique_code
            solution_text += "\n```\n"

        return solution_text

    def merge_code_blocks(self, code_blocks):
        """Merge multiple code blocks into a single coherent piece of code."""
        # Track seen imports and constants
        seen_imports = set()
        seen_constants = set()
        final_code = []
        
        for block in code_blocks:
            lines = block.split('\n')
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Handle imports
                if line.startswith('import ') or line.startswith('from '):
                    if line not in seen_imports:
                        seen_imports.add(line)
                        final_code.append(line)
                # Handle constants (assumed to be in ALL_CAPS)
                elif re.match(r'^[A-Z][A-Z0-9_]*\s*=', line):
                    if line not in seen_constants:
                        seen_constants.add(line)
                        final_code.append(line)
                # Add all other lines
                else:
                    final_code.append(line)
        
        return '\n'.join(final_code)
