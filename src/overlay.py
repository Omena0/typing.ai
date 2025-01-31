import customtkinter as tki
from screeninfo import screeninfo
import keyboard as kb
PAUSE = 0

width = screeninfo.get_monitors()[0].width
height = screeninfo.get_monitors()[0].height

tki.set_appearance_mode('system')

root = tki.CTk(fg_color='black')
root.title('Typing.ai')
root.wm_attributes("-transparentcolor", "black",'-topmost',True,'-fullscreen',True)
root.overrideredirect(True)
root.geometry(f'{width}x{height}')

gui_shown = False

tb = tki.CTkEntry(
    root,
    width = 500,
    height = 50,
    corner_radius = 6,
    font = tki.CTkFont(size=20)
)


def toggle_gui():
    global gui_shown
    if gui_shown:
        tb.place_forget()
    else:
        tb.place(relx=0.5,rely=0.4,anchor='center')
        root.lift()
        tb.lift()
        tb.focus_set()
        tb.focus_force()

    gui_shown = not gui_shown

def setKeybind(keybind):
    kb.add_hotkey(keybind, toggle_gui, suppress=False)
