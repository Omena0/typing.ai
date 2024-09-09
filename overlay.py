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

frame = tki.CTkFrame(root,width=width,height=height,bg_color='black',fg_color='black',border_color='black')
frame.place(x=0,y=0)

tb = tki.CTkEntry(
    frame,
    width = 500,
    height = 50,
    corner_radius = 6,
    font = tki.CTkFont(size=20)
)
tb.place(x=width/2-250,y=height/2-25)

frame.place_forget()

def toggle_gui():
    global gui_shown
    if gui_shown:
        frame.place_forget()
    else:
        frame.place_configure(x=0,y=0)
        root.lift()
        tb.lift()
        tb.focus_set()
        tb.focus_force()

    gui_shown = not gui_shown

kb.add_hotkey('tab',toggle_gui,suppress=True)
