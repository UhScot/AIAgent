import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter. If no arguments, run the file without any arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        raise Exception(f'Error: Cannot execute "{file_path}" as it is outside of the permitted working directory')
    
    if not os.path.isfile(abs_file_path):
        raise Exception(f'Error: File "{file_path}" not found')
    
    if not file_path.endswith('.py'):
        raise Exception(f'Error: "{file_path}" is not a Python file')

    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(commands,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory,
        )
        output = []
        
        if result.stdout:
            output.append(f'STDOUT:\n{result.stdout}')
        if result.stderr:
            output.append(f'STDERR:\n{result.stderr}')
        if result.returncode != 0:
            output.append(f'\nProcess exited with return code {result.returncode}')
        return "\n".join(output) if output else 'No output produced.'
    except Exception as e:
        return f'Error executing Python file: {e}'