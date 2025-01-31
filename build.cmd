
rem Nuitka compile
py -m nuitka --standalone --enable-plugin=tk-inter^
 --product-name="Typing.ai" --product-version=1.0.4^
 --file-description="A useful AI assistant"^
 --copyright="Copyright © 2025 Omena0. All rights reserved."^
 --output-dir="build"^
 --include-package-data="customtkinter"^
 --deployment --python-flag="-OO" --python-flag="-S"^
 --output-filename="typing.ai_main.exe"^
 --include-data-files=src/resources/icon.png=resources/icon.png^
 --include-data-files=src/system.md=system.md^
 --windows-icon-from-ico=src/resources/icon.png^
 --windows-console-mode=disable^
 --lto=no^
 src/main.pyw

rem mov to dist
cd build
powershell Compress-Archive main.dist main.zip
move "main.zip" "../dist/main.zip"
