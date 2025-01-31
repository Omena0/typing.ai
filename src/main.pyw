from threading import Thread
import commands as commands
import overlay as overlay
import keyboard as kb
from PIL import Image
from tools import *
import configLib
import pystray
import ollama
import os

VERSION = '1.0.4'

print(f'typing.ai v{VERSION}')
print('Created by Omena0\n')

# Create system tray icon
icon = pystray.Icon(
    'typing.ai',
    Image.open('resources/icon.png'),
    menu=pystray.Menu(
        pystray.MenuItem(
            'Open',
            overlay.toggle_gui
        ),
        pystray.MenuItem(
            'Github',
            lambda: webbrowser.open('https://github.com/Omena0/typing.ai/')
        ),
        pystray.MenuItem(
            'About',
            lambda: tkinter.messagebox.Message(
                overlay.root,
                title='About',
                message=f'Version: {VERSION}\nCopyright © 2025 Omena0.\nAll rights reserved.',
                type=tkinter.messagebox.OK
            ).show()
        ),
        pystray.MenuItem(
            'Help',
            lambda: tkinter.messagebox.Message(
                overlay.root,
                title='Help',
                message=f"Press '{config.general.hotkey}' to open.\n\n{commands.help}",
                type=tkinter.messagebox.OK
            ).show()
        ),
        pystray.MenuItem(
            'Quit',
            overlay.root.quit
        )
    )
)


# Set default config
configLib.setDefault(
"""
[General]
model = "deepseek-r1"
hotkey = "caps lock"
"""
)

if (ROAMING := os.getenv('appdata')) is None: # Get appdata/roaming folder, raise error if not found
    tkinter.messagebox.showerror('Error','Could not find appdata folder.\n\nos.getenv("appdata") returned None.')
    print('Could not find appdata folder.\n\nos.getenv("appdata") returned None.')
    exit(1)

configPath = os.path.join(ROAMING, 'typing.ai', 'config.ini')

# Parse config
config = configLib.parse(configPath)

# Set model and hotkey
model = config.general.model or 'deepseek-r1'

overlay.setKeybind(config.general.hotkey or 'caps lock')


def load_system():
    global system
    with open('system.md') as f:
        system = f.read().strip()

def generate(text:str|None):
    load_system()

    history = [{"role":"system","content":system},{"role": "user", "content": text}]

    stream = ollama.chat(
        model,
        history,
        stream=True,
        options={"num_ctx": len(system)+len(text)+100}
    )

    response = ''

    for chunk in stream:
        response += chunk.message.content
        print(chunk.message.content,end='')

    return response

def messagebox(title:str,message:str):
    """Create a message box in a new thread

    Args:
        title (str): Title of the msgbox
        message (str): Message of the msgbox
    """
    Thread(
        target=tkinter.messagebox.showinfo,
        args=(title,message)
    ).start()

def complete(text:str):  # sourcery skip: use-named-expression
    # Check if command
    if text.startswith(tuple(commands.commands.keys())):
        return commands.parse(text)

    # Otherwise AI
    print(f'Generating... [{text}]')

    response = generate(text)

    # Remove <think> and tool calling
    user_response = response.rsplit('</think>',1)[1].rsplit('TOOL_CALLS',1)[0].strip()

    # Send user response if exists
    if user_response:
        messagebox('Response:', user_response)

    # Tool calls escape
    response = response.replace('\\TOOL_CALLS','')

    # Run tool calls if exists
    if 'TOOL_CALLS:' in response:
        # Parse every line after 'TOOL_CALLS:' as tool call
        for tool in response.rsplit('TOOL_CALLS:',1)[1].split('\n'):
            tool = tool.strip()
            if not tool:
                continue

            # Simply eval the tool call (couldnt bother parsing frfr)
            try:
                eval(tool,globals=tool_functions, locals={})
            except Exception as e:
                # Optionally show errors, gets annoying since it makes a lot of them lmfao
                #tkinter.messagebox.showerror('Error',f'Error: {e}')
                print(f'Error: {e}')

    # Done :D
    print('\nDone')

def send(*_):
    if overlay.gui_shown:
        text = overlay.tb.get()
        overlay.tb.delete(0,overlay.tki.END)
        overlay.toggle_gui()
        complete(text)
        overlay.gui_shown = False

kb.add_hotkey('enter',send)

print('Ready.')

# Start icon
Thread(target=icon.run,daemon=True).start()

# Start tkinter
overlay.root.mainloop()

# Cleanly quit icon
icon.stop()
