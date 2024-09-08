import subprocess
import webbrowser


def run_command(command:str):
    command = command.strip()
    print(command)
    try:
        subprocess.check_output(f'cmd /C {command}'.split(' ')).decode(errors='ignore')
    except Exception as e:
        return f'Error: {e}'

def run_code(code:str):
    return eval(code,globals(),globals())

def open_website(url:str):
    webbrowser.open(url,2)

tools_list = [
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
            'name': 'run_code',
            'description': 'Run python code.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'command': {
                        'type': 'string',
                        'description': 'The command to run',
                    }
                },
                'required': ['code'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'open_website',
            'description': 'Open a website.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'url': {
                        'type': 'string',
                        'description': 'The url to open.',
                    }
                },
                'required': ['url'],
            },
        },
    }
]

tool_functions = {
    'run_command': run_command,
    'run_code': run_code,
    'open_website': open_website
}
