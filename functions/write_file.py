from pathlib import Path

from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites files in the specified directory, constrained to the working directory.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write or overwrite the content to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    wd = Path(working_directory).resolve()
    fp = (wd / file_path).resolve()

    if not fp.is_relative_to(wd):
        return f'Error: Cannot write to "{fp}" as it is outside the permitted working directory'

    if not fp.is_file():
        try:
            fp.touch()
        except Exception as e:
            return f"Error: failed to create file: {e}"

    try:
        with open(fp, "wt") as f:
            num_written = f.write(content)
        return f'Successfully wrote to "{fp}" ({num_written} characters written)'
    except Exception as e:
        return f"Error: could not write to '{fp}': {e}"



