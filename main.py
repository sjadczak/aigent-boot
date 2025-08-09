import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "Why is the sky blue?" [--verbose]')
        sys.exit(1)


    verbose = False
    if len(sys.argv) == 3:
        verbose = sys.argv[2].lower() == "--verbose"

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose:
        print(f"User prompt: {user_prompt}")

    print(resp.text)

    if verbose:
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
