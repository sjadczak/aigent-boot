from pathlib import Path

from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory="calculator", directory="."):
    wd = Path(working_directory).resolve()
    path = (wd / directory).resolve()

    if not path.is_relative_to(wd):
        return f'Error: cannot list "{directory}" as it is outside the permitted working directory'

    if not path.is_dir():
        return f'Error: "{directory}" is not a directory'
    
    try:
        file_info = []
        for p in path.iterdir():
            line = f" - {p.name}: file_size={p.stat().st_size} bytes, is_dir={p.is_dir()}"
            file_info.append(line)

        return "\n".join(file_info)
    except Exception as e:
        return f"Error listing files: {e}"
