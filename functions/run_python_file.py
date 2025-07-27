import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    requested_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if requested_path.startswith(working_path) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(requested_path) == False:
        return f'Error: File "{file_path}" not found.'
    if file_path.endswith(".py") == False or os.path.isfile(requested_path) == False:
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python", file_path] + args, text=True, capture_output=True, timeout=30, cwd=working_path)
        if not result.stdout and not result.stderr:
            return "No output produced."
        if result.returncode != 0:
            return f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}\nProcess exited with code {result.returncode}"
        return f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to get the python file from, relative to the working directory. If not provided, try the file in the working directory itself.",
            ),
        },
    ),
)