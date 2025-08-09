import subprocess

from pathlib import Path


def run_python_file(working_directory, file_path, args=None):
    if not args:
        args = []

    wd = Path(working_directory).resolve()
    fp = (wd / file_path).resolve()

    if not fp.is_relative_to(wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not fp.exists():
        return f'Error: File "{file_path}" not found.'

    if fp.suffix != ".py":
        return f'Error: "{fp}" is not a Python file.'

    try:
        cmd = ["python3", fp, *args]
        result = subprocess.run(
            cmd,
            timeout=30,
            capture_output=True,
            cwd=wd, 
        )
        
        rv = ""

        if stdout := result.stdout:
            rv += f'STDOUT: \n"\n{stdout.decode("utf-8")}\n"\n\n'

        if stderr := result.stderr:
            rv += f'STDERR: \n"\n{stderr.decode("utf-8")}\n"\n\n'
        
        if code := result.returncode:
            rv += f' Process exited with code {code}\n'

        if not rv:
            rv = "No output produced."

        return rv
    except Exception as e:
        return f'Error: executing python file: {e}'
