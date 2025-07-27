import os
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

import sys

from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    if len(sys.argv) == 1:
        print("Please type in prompt!")
        sys.exit(1)
    
    # Check for verbose flag
    verbose = "--verbose" in sys.argv
    
    # Get the prompt, excluding the --verbose flag
    prompt_args = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    user_prompt = " ".join(prompt_args)
    
    if verbose:
        print(f"User prompt: {user_prompt}")
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
