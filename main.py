import json

from agent.agent import callLLM
from agent.file_utils import createFile, readFile, listFilesRecursive,replaceFileContent,deleteFile
from agent.command_runner import runCommand
from rich.prompt import Prompt
from rich.console import Console

console = Console()

messages = []

avaiable_tools = {
    "createFile": {
        "fn": createFile,
    },
    "readFile": {
        "fn": readFile,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
    "replaceFileContent": {
        "fn": replaceFileContent,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
    "deleteFile": {
        "fn": deleteFile,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
}


def loadSystemPrompt():
    with open("prompts/system_prompt.txt") as f:
        return {"role": "system", "content": f.read()}


def showFileIndex():
    files = listFilesRecursive()
    if files:
        console.print("[bold cyan]Project Files:[/]")
        for f in files:
            console.print(f"  - {f}")


def main():
    console.print("[bold green]AI Coding Agent (Terminal)[/]")
    messages.append(loadSystemPrompt())

    while True:
        user_input = Prompt.ask("\n> What would you like to do? or quit")
        if user_input == 'quit':
            break
        messages.append({"role": "user", "content": user_input})

        while True:
            response = callLLM(messages)

            parsed_output = json.loads(response)
            messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

            if parsed_output.get("step") == "plan":
                print(f"{parsed_output.get('content')}")
                continue

            if parsed_output.get("step") == "action":
                tool_name = parsed_output.get("function")

                if tool_name == 'runCommand':
                    tool_input = parsed_output.get("input")
                    if avaiable_tools.get(tool_name, False):
                        output = avaiable_tools[tool_name].get("fn")(tool_input)
                        messages.append(
                            {"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                        continue
                if tool_name == 'readFile':
                    tool_input = parsed_output.get("path")
                    if avaiable_tools.get(tool_name, False):
                        output = avaiable_tools[tool_name].get("fn")(tool_input)
                        messages.append(
                            {"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                        continue

                if tool_name == 'createFile':
                    path = parsed_output.get("path")
                    content = parsed_output.get("content")
                    if avaiable_tools.get(tool_name, False):
                        output = avaiable_tools[tool_name].get("fn")(path,content)
                        messages.append(
                            {"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                        continue

                if tool_name == 'replaceFileContent':
                    path = parsed_output.get("path")
                    new_content = parsed_output.get("content")
                    if avaiable_tools.get(tool_name, False):
                        output = avaiable_tools[tool_name].get("fn")(path,new_content)
                        messages.append(
                            {"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                        continue

            if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get('content')}")
                break




if __name__ == "__main__":
    main()
