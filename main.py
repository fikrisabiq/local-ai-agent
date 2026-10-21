import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from config import MAX_ITERATION
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("API Key is empty")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def generate_response(messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    return response.choices[0].message

def main():
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    success = False

    for _ in range(MAX_ITERATION):
            message = generate_response(messages)
            messages.append(message)

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, args.verbose)
                    if not result_message.get("content"):
                        raise Exception("Content have no content")
                    if args.verbose:
                        print(f"-> {result_message['content']}")

                    messages.append(result_message)
            else:
                print("Final response:")
                print(message.content)
                success = True
                break

    if not success:
        print("Error: Reached maximum iterations without a final response.")
        sys.exit(1)

if __name__ == "__main__":
    main()
