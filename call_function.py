from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(fn_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {fn_call_part.name}({fn_call_part.args})")
    else:
        print(f" - Calling function: {fn_call_part.name}")
    fn_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    fn_name = fn_call_part.name
    if fn_name not in fn_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"error": f"Unknown function: {fn_name}"},
                )
            ],
        )
    args = dict(fn_call_part.args)
    args["working_directory"] = WORKING_DIR
    fn_result = fn_map[fn_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fn_name,
                response={"result": fn_result},
            )
        ],
    )
