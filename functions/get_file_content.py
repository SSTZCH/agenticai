import os
from google import genai
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

    requested_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)

    if requested_path.startswith(working_path) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(requested_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(requested_path, "r") as f:
            if os.path.getsize(requested_path) > MAX_CHARS:
                file_content_string = f.read(MAX_CHARS) + f"[...File {file_path} truncated at 10000 characters]"
            else:
                file_content_string = f.read()
        return file_content_string

    except Exception as e:
            return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a specified file, at a maximum of 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to get the file from, relative to the working directory. If not provided, try the file in the working directory itself.",
            ),
        },
    ),
)