import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):

    requested_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if requested_path.startswith(working_path) == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        dir_path = os.path.dirname(requested_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(requested_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory where the file is to be located, relative to the working directory. If not provided, try the working directory itself.",
            ),
        },
    ),
)