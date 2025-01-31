import urllib.parse
import webbrowser
import os

prefixes = {
    'search ': lambda x: webbrowser.open(f'https://www.google.com/search?q={urllib.parse.quote_plus(x)}'),
    '.': lambda x: os.system(x),
    'https://': lambda x: webbrowser.open(f'https://{x}'),
    'http://': lambda x: webbrowser.open(f'http://{x}'),
}

def parse(text:str):
    for prefix, callback in prefixes.items():
        if text.startswith(prefix):
            return callback(text.removeprefix(prefix))


