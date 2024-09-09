import keyboard as kb
from tools import *
import overlay
import ollama
import pyautogui

model = 'allenporter/xlam:1b'

system = r"""
Use the tools provided to do what the user wants.

Tools usage:
- run_command: Open an application on the user's machine, the user wants to open a program.
- run_code: Perform math operations, use this only when the user wants to perform math operations.
- open_website: Open websites, use this only when the user wants to open a website, or search something.
- type_text: Type text, use this only when the user wants output from you, and no other tool matches the job.

Remember to add quotes when trying to open programs, or the command wont work.

Use the start command to start programs

If the user asks you to google something, run the open_website tool with the url: "https://google.com/search?q=<QUERY>"

Examples (THESE ARE EXAMPLES; YOU DONT HAVE TO USE THEM!):
- "open adobe photoshop":
    You should use command "run_command" with command 'start "C:\Program Files\Adobe\Adobe Photoshop 2021\photoshop.exe"'

- "google python 3.12":
    You should use command "open_website" with "https://google.com/search?q=python+3.12"

- "what's 9 + 10":
    You should use command "run_code" with "9+10", the result will be typed on the user's current focused text document.

- "explain quantum mechanics to a 7 year old":
    You should use command "type_text" with "Quantum mechanics is like a set of magical rules that describe how tiny things, like atoms and particles, behave. Imagine you're in a world where things can be in two places at once, or where something only happens when you look at it. It's like a game with strange but cool rules that are different from the ones we see every day. Scientists use these rules to understand how everything works at the smallest level."

Respond in json.
Platform: Windows 10 x64
"""

def generate(text:str|None):

    history = [{"role":"system","content":system},{"role": "user", "content": text}]

    return ollama.chat(
        model,
        history,
        options={"temperature": 1.25, "top_k": 65, "top_p": 0.8, "n_ctx": len(system)+100},
        tools=tools_list,
        format='json'
    )

def complete(text):
    print(f'Generating... [{text}]')

    response = generate(text)

    if response['message'].get('tool_calls'):
        for tool in response['message']['tool_calls']:
            print(f'Calling: {tool['function']['name']}({tool["function"]["arguments"]})')

            func = tool_functions[tool['function']['name']]

            args = tool['function']['arguments'].values()

            try: tool_result = func(*args)
            except Exception as e:
                print(e)
                return

            print(f'Result: {tool_result}')

            if tool_result:
                pyautogui.typewrite(tool_result)

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

