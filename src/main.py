from threading import Thread
import commands as commands
import overlay as overlay
import keyboard as kb
from tools import *
import configLib
import ollama

configLib.setDefault(
"""
[General]
model = "deepseek-r1"
hotkey = "caps lock"
"""
)

config = configLib.parse('config.ini')

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
    Thread(
        target=tkinter.messagebox.showinfo,
        args=(title,message)
    ).start()

def complete(text:str):  # sourcery skip: use-named-expression
    if text.startswith(tuple(commands.prefixes.keys())):
        return commands.parse(text)

    print(f'Generating... [{text}]')

    response = generate(text)

    user_response = response.rsplit('</think>',1)[1].rsplit('TOOL_CALLS',1)[0].strip()

    if user_response:
        messagebox('Response:', user_response)

    response = response.replace('\\TOOL_CALLS','')

    if 'TOOL_CALLS:' in response:
        for tool in response.rsplit('TOOL_CALLS:',1)[1].split('\n'):
            tool = tool.strip()
            if not tool:
                continue

            try:
                eval(tool,globals=tool_functions, locals={})
            except Exception as e:
                #tkinter.messagebox.showerror('Error',f'Error: {e}')
                print(f'Error: {e}')

    print('\nDone')


def send(*_):
    if overlay.gui_shown:
        text = overlay.tb.get()
        overlay.tb.delete(0,overlay.tki.END)
        overlay.toggle_gui()
        complete(text)
        overlay.gui_shown = False

kb.add_hotkey('enter',send)

overlay.root.mainloop()


