# Gemini Prompt Library Ideator

A tool for generating prompt libraries for use with Large Language Models (LLMs) like Gemini, particularly designed for Open Web UI integration.

## Overview

This tool uses the Gemini API to generate collections of prompts based on user-specified topics. It's designed to help create prompt libraries that can be easily accessed via slash commands in Open Web UI, reducing repetitive data entry when interacting with LLMs.

## Features

- **Interactive Prompt Generation**: Specify the topic and number of prompts you want to generate
- **Descriptive Filenames**: Automatically creates filenames based on the prompt topic
- **Dedicated Output Folder**: Saves all generated prompts in a "created-prompts" folder
- **Multiple Output Formats**: Generates both JSON and CSV formats for easy importing
- **Variable Formatting**: Uses double curly brackets for variables (e.g., `{{variable_name}}`)
- **Customizable**: Easily modify the system prompt to change the style of generated prompts

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip install google-generativeai python-dotenv
   ```
4. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY="your_api_key_here"
   ```

## Usage

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Run the prompt generator:
   ```bash
   cd as-code/v2
   python prompt.py
   ```

3. Follow the interactive prompts:
   - Enter the type of prompts you want to generate (e.g., "Python programming", "Job search")
   - Specify how many prompts you want to generate
   - Choose whether to view the generated prompts after creation

4. The generated prompts will be saved in the `created-prompts` folder in both JSON and CSV formats with descriptive filenames (e.g., `python-programming-prompts.json`).

## Example Output

The tool generates prompts in this format:

```json
[
  {
    "Prompt name": "Formal Tone",
    "Prompt text": "Rewrite the following text in a formal tone: {{text}}",
    "Slash command": "/formalize"
  },
  {
    "Prompt name": "Simplify Text",
    "Prompt text": "Simplify the following text, making it easier to understand: {{text}}",
    "Slash command": "/simplify"
  }
]
```

## Project Structure

- `as-code/v2/prompt.py`: Main script for generating prompts
- `created-prompts/`: Directory containing all generated prompt files
- `.env`: Environment file for storing your Gemini API key

## License

MIT
