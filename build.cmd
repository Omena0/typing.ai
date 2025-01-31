
rem Nuitka compile
py -m nuitka --standalone --onefile --enable-plugin=tk-inter^
 --product-name="Typing.ai" --product-version=1.0.0 --file-description="A useful AI assistant" --copyright="Copyright © 2025 Omena0. All rights reserved."^
 --output-dir="build"^
 --include-package-data="customtkinter"^
 --deployment --python-flag="-OO" --python-flag="-S"^
 --output-filename="typing.ai_main.exe"^
 src/main.py

rem mov to dist
cd build
move "typing.ai_main.exe" "../dist/typing.ai_main.exe"
