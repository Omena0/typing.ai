import subprocess
import webbrowser
import tkinter.messagebox
from pyautogui import typewrite

def run_command(command:str):
    command = command.strip()
    print(command)
    try:
        subprocess.check_output(f'cmd /C {command}'.split(' ')).decode(errors='ignore')
    except Exception as e:
        err = f'Error: {e}'
        tkinter.messagebox.showerror('Error', err)
        return err

def run_code(code:str):
    return eval(code,globals(),globals())

def open_website(url:str):
    if url == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ':
        tkinter.messagebox.showerror('Bruh',"The AI has tried to rickroll you, I've saved you from this...\n\nThis USUALLY means your request is unclear.")
        return
    webbrowser.open(url,2)

def type_text(text:str):
    typewrite(text,0.05,_pause=False)

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
    },
    {
        'type': 'function',
        'function': {
            'name': 'type_text',
            'description': 'Types text.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'The text to type.',
                    }
                },
                'required': ['text'],
            },
        },
    }
]

tool_functions = {
    'run_command': run_command,
    'run_code': run_code,
    'open_website': open_website,
    'type_text': type_text,
}
