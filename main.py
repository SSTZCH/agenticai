import os
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

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

function_map = {
    "get_files_info": get_files_info, 
    "get_file_content": get_file_content, 
    "run_python_file": run_python_file, 
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_name = function_call_part.name
    func = function_map.get(function_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    try:
        args = function_call_part.args.copy()
        args["working_directory"] = "./calculator"
        function_result = func(**args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
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
    
    for _ in range(20):
        response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        
        for candidate in response.candidates:
            messages.append(candidate.content)

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                result_content = types.Content(role="user", parts=function_call_result.parts)
                messages.append(result_content)
                if len(function_call_result.parts) == 0:
                    raise Exception("No function_response parts!")
                if not hasattr(function_call_result.parts[0], "function_response"):
                    raise Exception("No function_response attribute!")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            break  # Stop looping if there are no function calls (final answer reached)

if __name__ == "__main__":
    main()
