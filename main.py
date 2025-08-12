import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

fns = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

 - List files and directories
 - Read file contents
 - Execute Python files with optional arguments
 - Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def call_function(fn_call, verbose=False):
    if verbose:
        print(f"Calling function: {fn_call.name}({fn_call.args})")
    else:
        print(f" - Calling function: {fn_call.name}")

    fn_call.args["working_directory"] = "./calculator"
    fn = fns.get(fn_call.name)
    if not fn:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_call.name,
                    response={"error": f"Unknown function: {fn_call.name}"},
                ),
            ],
        )
    result = fn(**fn_call.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fn_call.name,
                response={"result": result},
            ),
        ],
    )

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "Why is the sky blue?" [--verbose]')
        sys.exit(1)


    verbose = False
    if len(sys.argv) == 3:
        verbose = sys.argv[2].lower() == "--verbose"

    user_prompt = sys.argv[1]

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        ),
    ]

    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if verbose:
        print(f"User prompt: {user_prompt}")

    if resp.function_calls:
        for fc in resp.function_calls:
            res = call_function(fc)
            if rc := res.parts[0].function_response.response:
                if verbose:
                    print(f" -> {rc}")
            else:
                raise Exception(f"Unknown error calling {fc.name}")


    print(resp.text)

    if verbose:
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
