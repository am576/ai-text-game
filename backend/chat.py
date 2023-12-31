import requests
import json
import time

url = "http://localhost:11434/api/chat"
data = {
    "model": "dolphin",
    "messages": [
        {
            "role": "user",
            "content": "why is the sky blue?"
        }
    ]
}

def chat(messages):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "dolphin",
        "messages": messages
    }

    response = requests.post(url, json=data, stream=True)

    output = ""
    for line in response.iter_lines():
        body = json.loads(line)
        if line:
            # Parse the line as a JSON object
            
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)
            # Print the response object
        if body.get("done", False):
            message["content"] = output
            return message
    


def main():
    messages = []

    while True:
        user_input = input("Enter a prompt: ")
        if not user_input:
            exit()
        print()
        messages.append({"role": "user", "content": user_input})
        start = time.time()
        message = chat(messages)
        end = time.time()
        execution_time = end - start

        # Print the execution time
        print(f"\nExecution time: {round(execution_time, 1)} seconds")
        messages.append(message)
        print("\n\n")


if __name__ == "__main__":
    main()