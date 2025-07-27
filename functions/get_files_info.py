import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory=None):

    requested_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)

    if requested_path.startswith(working_path) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(requested_path) == False:
        return f'Error: "{directory}" is not a directory'
    
    try:
        items = os.listdir(requested_path)
        strings = []
        for item in items:
            item_path = os.path.join(requested_path, item)
            strings.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        return "\n".join(strings)
    except Exception as e:
            return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)