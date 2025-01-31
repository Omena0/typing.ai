from pyautogui import getAllWindows
import urllib.parse
import webbrowser
import AppOpener
import os

def _close(x:str):
    if not x.strip(): return
    for window in getAllWindows():
        if x in window.title:
            window.close()
            break

def _open(x:str):
    if not x.strip(): return
    AppOpener.open(x)

commands = {
    '.search ': lambda x: webbrowser.open(f'https://www.google.com/search?q={urllib.parse.quote_plus(x)}'),
    '.cmd ': lambda x: os.system(x),
    '.open ': _open,
    '.close ': _close,
    '!': _close,
    'https://': lambda x: webbrowser.open(f'https://{x}'),
    'http://': lambda x: webbrowser.open(f'http://{x}'),
}

help = """
Commands:
.search <query> - Search Google.
<url> - Open URL. (http:// or https://)
.cmd <command> - Run shell command.
.open <app> - Open an application.
.close <app> - Close an application. (Alias: !<app>)
<prompt> - Prompt the AI.
""".strip()

def parse(text:str):
    for prefix, callback in commands.items():
        if text.startswith(prefix):
            return callback(text.removeprefix(prefix))


