import os
import config
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specific file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory."
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            )
        }
    )
)



def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)

    if not os.path.abspath(full_path).startswith(abs_path):
        raise Exception(f'Error: Cannot write to "{file_path}" as it is outside of the permitted working directory')
        
    try:
        with open(full_path, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'