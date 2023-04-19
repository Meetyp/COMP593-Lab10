from tkinter import *
from tkinter import ttk
import os
import ctypes
import poke_api
import image_lib

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__) 
script_dir = os.path.dirname(script_path)

#Create image cache directory
image_cache_dir= os. path.join(script_dir, 'images')
if not os.path.isdir (image_cache_dir):
    os.makedirs(image_cache_dir)

# Create the main window
root = Tk() 
root.title("Pokemon Image Viewer")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.minsize(500, 600)

# Set the window icon
icon_path = os.path.join(script_dir, 'Poke-Ball.ico')
root.iconbitmap(icon_path)

# Set the Taskbar icon
app_id = 'COMP593.PokeImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


# Put a frame on the GUI
frame = ttk.Frame(root)
frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)
frame.rowconfigure(0, weight=100)
frame.columnconfigure(0, weight=100)

# Put image into frame
image_path = os.path.join(script_dir, 'logo.png')
img_poke = PhotoImage(file=image_path)
lbl_image = ttk.Label(frame, image=img_poke)
lbl_image.grid(padx=10, pady=10)

# Put the Pull-Down of Pokemon names into the frame
pokemon_name_list = sorted(poke_api.get_pokemon_names())
cbox_pokemon_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_pokemon_names.set("Select an Pokemon")
cbox_pokemon_names.grid(padx=10, pady=(10, 0))

def handle_pokemon_sel(event):
    sel_pokemon = cbox_pokemon_names.get()
    global image_path
    image_path = poke_api.dowload_pokemon_artwork(sel_pokemon, image_cache_dir)
    img_poke['file'] = image_path
    btn_set_desktop.state(['!disabled'])
    return

cbox_pokemon_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)

# Put "Set Desktop" button into frame
def handel_set_desktop():
    image_lib.set_desktop_background_image(image_path)
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image', state=DISABLED, command=handel_set_desktop)
btn_set_desktop.grid(padx=10, pady=(10, 20))

root.mainloop()