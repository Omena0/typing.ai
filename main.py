import keyboard as kb
import overlay
import ollama
import subprocess

model = 'mistral:7b-instruct-v0.3-q2_K'

system = """\
Use the tools provided to do what the user wants.
Respond in json.
Only run one command at a time.
Platform: Windows 10 x64
"""

history = [
    {"role":"system","content":system}
]

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'run_command',
            'description': 'Run a command with system shell.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'command': {
                        'type': 'string',
                        'description': 'The command to run',
                    }
                },
                'required': ['command'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'eval',
            'description': 'Run python code.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'command': {
                        'type': 'string',
                        'description': 'The command to run',
                    }
                },
                'required': ['command'],
            },
        },
    }
]

def run_command(command:str):
    command = command.strip()
    print(command)
    try:
        return subprocess.check_output(f'cmd /C {command}'.split(' ')).decode(errors='ignore')
    except Exception as e:
        return f'Error: {e}'

def generate(text:str|None):

    if text: history.append({"role": "user", "content": text})

    resp = ollama.chat(
        model,
        history,
        options = {"temperature": 0.3},
        tools = tools,
        format = 'json'
    )

    return resp

def complete(text):
    print(f'Generating... [{text}]')

    response = generate(text)

    content = response['message']['content']

    if response['message'].get('tool_calls'):
        available_functions = {
            'run_command': run_command,
            'eval': eval
        }

        for tool in response['message']['tool_calls']:
            print(f'Calling: {tool['function']['name']}({tool["function"]["arguments"]["command"]})')

            function_to_call = available_functions[tool['function']['name']]

            arg = tool['function']['arguments']['command']

            function_response = function_to_call(
                arg
            )

            # Add function response to the conversation
            history.append(
                {
                    'role': 'tool',
                    'content': function_response,
                }
            )

    print('\nDone')


def send(*_):
    if overlay.gui_shown:
        text = overlay.tb.get()
        overlay.tb.delete(0,overlay.tki.END)
        overlay.toggle_gui()
        complete(text)

kb.add_hotkey('enter',send)

overlay.root.mainloop()

