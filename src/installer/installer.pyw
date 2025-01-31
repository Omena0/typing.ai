from tkinter import PhotoImage, messagebox
from threading import Thread
import customtkinter as tki
from time import sleep
import urllib.request
import os

if (ROAMING := os.getenv('appdata')) is None: # Get appdata/roaming folder, raise error if not found
    messagebox.showerror('Error','Could not find appdata folder.\n\nos.getenv("appdata") returned None.')
    print('Could not find appdata folder.\n\nos.getenv("appdata") returned None.')
    exit(1)

root = tki.CTk()
root.title('typing.ai Installer')
root.geometry('400x250')

title = tki.CTkLabel(root, text='typing.ai', font=(None, 40, 'bold'))
title.pack()

desc = tki.CTkLabel(root, text='Press "Install" to install typing.ai.', font=(None, 20, 'bold'))
desc.pack(pady=5)

button = tki.CTkButton(
    root,
    text='Install',
    font=(None, 20, 'bold'),
    command=lambda: (
        Thread(target=install_thread, daemon=True).start()
    )
)
button.pack(pady=10)

progress = tki.CTkProgressBar(root, width=200, mode='indeterminate')
progress.pack(pady=20)
progress.start()

def install_thread():
    progress.configure(mode='determinate')
    progress.stop()
    progress.set(0)

    # Create directory
    install_dir = os.path.join(ROAMING, 'typing.ai')
    os.makedirs(install_dir, exist_ok=True)
    progress.step()

    # Download files
    temp_dir = os.path.join(install_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    urllib.request.urlretrieve()

icon = PhotoImage(file='resources/icon.png')
def setIcon():
    for _ in range(100):
        sleep(0.00000000000000000000000000000000000001)
        root.iconphoto(False, icon)

Thread(target=setIcon,daemon=True).start()

root.mainloop()
