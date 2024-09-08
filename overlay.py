import customtkinter as tki
from screeninfo import screeninfo
import keyboard as kb
PAUSE = 0

x = screeninfo.get_monitors()[0].width
y = screeninfo.get_monitors()[0].height



root = tki.CTk(fg_color='black')
root.title('Typing.ai')
root.wm_attributes("-transparentcolor", "black",'-topmost',True,'-fullscreen',True)
root.overrideredirect(True)
root.geometry(f'{x}x{y}')

gui_shown = False

frame = tki.CTkFrame(root,width=x,height=y,bg_color='black',fg_color='black',border_color='black')
frame.place(x=0,y=0)

tb = tki.CTkEntry(
    frame,
    width = 500,
    height = 50,
    corner_radius = 6,
    font = tki.CTkFont(size=20)
)
tb.place(x=x/3-135,y=y/3)

frame.place_forget()

def toggle_gui():
    global gui_shown
    gui_shown = not gui_shown
    if not gui_shown:
        frame.place_forget()
    else:
        frame.place_configure(x=0,y=0)
        tb.lift()
        tb.focus_set()

kb.add_hotkey('tab',toggle_gui,suppress=True)
