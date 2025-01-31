import requests

with open('version.txt') as f:
    version = f.read().strip()

requests.get('https://raw.githubusercontent.com/Omena0/typing.ai/refs/heads/main/VERSION.txt')

