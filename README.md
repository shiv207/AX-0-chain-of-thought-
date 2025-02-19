# AX-O: Replicating O1's Chain of Thought Reasoning

> **Original Concept**: This project is based on the work by [Prompt Engineering](https://youtu.be/Oasl9rSJNds). We have made several modifications to enhance efficiency and improve response accuracy in attempting to replicate O1's capabilities.

## Project Description

This project is a **modified implementation** that aims to replicate the reasoning capabilities of OpenAI's newly released O1 model. O1 uses chain-of-thought prompting and reinforcement learning to reflect on its solutions, improving responses through iterative reasoning. Our goal is to mimic this behavior using alternative models, with several enhancements to improve efficiency and response accuracy.

In this implementation, we use a sequential agent-based system powered by the Gemini API (or any model with function-calling capabilities). The system proposes solutions to coding-related problems and iteratively refines them using chain-of-thought and reflection techniques at each stage. The Gemini API, with its code execution abilities, is ideal for this project. While it works with Gemini Flash, we recommend using the Pro version to avoid issues with external package dependencies, as the Pro version generally sticks to Python's standard library.

### Key Modifications from Original
- Enhanced efficiency in agent interactions
- Improved response accuracy through refined prompting
- Modified chain-of-thought implementation for better reasoning
- Optimized for coding-related problem-solving

## Important Note

This is a **modified version** of the original concept and was enhanced to improve performance. While we've made several improvements, you may still encounter occasional issues. It currently works best for problems that can be solved through coding. We encourage you to give it a try and **report any bugs or issues** you encounter.

## How to Run

### 1. Set Environment Variable

You need to set an environment variable for your Google API key:
```bash
export GOOGLE_API_KEY=<your_api_key>
```

### 2. Create a Conda Virtual Environment

It's recommended to use a Conda environment for this project. To create and activate a new Conda environment:

```bash
conda create -n agent-0 python=3.10
conda activate agent-0
```

### 3. Install Dependencies

The only dependency required for this project is google-generativeai. Install it using pip:

```bash
pip install google-generativeai
```

### 4. Run the Script

```bash
python main.py
```

Give it a try and let us know what you think! Make sure to give it a star if you enjoyed it.

## Acknowledgments
Special thanks to [Prompt Engineering](https://youtu.be/Oasl9rSJNds) for the original concept and implementation that inspired this modified version.
