from pathlib import Path

from google.genai import types

from config import MAX_CHARS


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read contents from, relative to the working directory. If not provided, the function returns an error.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    wd = Path(working_directory).resolve()
    fp = (wd / file_path).resolve()

    if not fp.is_relative_to(wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not fp.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(fp, "rt") as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS]
                content += f'[...File "{fp}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: could not read file: {e}"
