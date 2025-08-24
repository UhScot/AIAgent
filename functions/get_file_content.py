import os
import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specific file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description="The file to retrieve content from, relative to the working directory."
            )
        }
    )
)

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)

    truncate = False

    if not os.path.abspath(full_path).startswith(abs_path):
        raise Exception(f'Error: Cannot read "{file_path}" as it is outside of the permitted working directory')
    
    if not os.path.isfile(full_path):
        raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
    
    try:
        if os.path.getsize(full_path) > config.MAX_CHARS:
            truncate = True
        with open(full_path, 'r') as file:
            if truncate:
                file_content = file.read(config.MAX_CHARS)
                file_content += f'\n[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
            else:
                file_content = file.read()

        return file_content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'