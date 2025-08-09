from pathlib import Path


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



