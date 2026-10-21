# functions/run_python_file.py

import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if absolute_file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
        text = []
        text.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            text.append("No output produced")
        if result.stdout:
            text.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            text.append(f"STDERR: {result.stderr}")
        return "\n".join(text)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file with optional command line arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of string arguments to pass to the script.",
                },
            },
            "required": ["file_path"],
        },
    },
}
