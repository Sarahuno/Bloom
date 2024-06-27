import pyautogui
import keyboard
import time
from pynput import mouse
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw

# Global variables
middle_button_clicked = False
hotkey_file = 'hotkey.txt'  # Text file where hotkey is stored
shikai_ressurection_file = 'shikai-resurrection.txt'  # Text file where hotkey is stored
hotkey = 'e'  # Default hotkey
hotkey_hooked = False  # Track if hotkey is currently hooked
action_performed = False  # Track if action has been performed
shikai = "Zangetsu"  # Default Shikai
app_title = 'Roblox' 

# Function to handle middle mouse button click events
def on_click(x, y, button, pressed):
    global middle_button_clicked
    if button == mouse.Button.middle and pressed:
        middle_button_clicked = not middle_button_clicked
        update_label()

# Function to update the label text in the GUI
def update_label():
    if middle_button_clicked:
        label.config(text="Mode : (Bankai)", fg='#ffffff', bg='#7289da')
    else:
        label.config(text="Mode : (Shikai)", fg='#ffffff', bg='#7289da')

# Function to handle hotkey press event
def on_hotkey_down(event):
    global action_performed
    if event.name == hotkey and not action_performed:
        if middle_button_clicked:
            execute_command('bankai')
        else:
            execute_command(f'bloom, {shikai}')
        action_performed = True

# Function to handle hotkey release event
def on_hotkey_up(event):
    global action_performed
    if event.name == hotkey:
        action_performed = False

# Function to bring the application window to the foreground
def focus_app_window():
    try:
        window = gw.getWindowsWithTitle(app_title)[0]
        window.activate()
        time.sleep(0.1)  # Wait a bit for the window to come to focus
    except IndexError:
        messagebox.showerror("Window Not Found", f"Could not find a window with the title '{app_title}'.")

# Function to execute command in the text field
def execute_command(command):
    focus_app_window()
    keyboard.press('/')
    keyboard.release('/')
    time.sleep(0.01)
    pyautogui.write(command)
    time.sleep(0.01)
    keyboard.press("enter")
    keyboard.release("enter")

# Function to read hotkey from text file
def read_hotkey():
    global hotkey
    try:
        with open(hotkey_file, 'r') as file:
            hotkey = file.read().strip()
            messagebox.showinfo("Hotkey Loaded", f"Hotkey loaded from file: '{hotkey}'")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"The file '{hotkey_file}' was not found. Using default hotkey.")

# Function to update hotkey listeners
def update_hotkey():
    global hotkey_hooked
    keyboard.unhook_all()
    initialize_hotkey()

# Initialize hotkey listeners
def initialize_hotkey():
    global hotkey_hooked
    keyboard.on_press_key(hotkey, on_hotkey_down)
    keyboard.on_release_key(hotkey, on_hotkey_up)
    hotkey_hooked = True

# Initialize Tkinter
root = tk.Tk()
root.title("Middle Button Click Status")
root.configure(bg='#36393f')
label = tk.Label(root, text="Mode : (Shikai)", font=("Arial", 12), fg='#ffffff', bg='#7289da', padx=10, pady=10)
label.pack(pady=20)
label2 = tk.Label(root, text=f"Current Shikai/Resurrection : {shikai}", font=("Arial", 12), fg='#ffffff', bg='#7289da', padx=10, pady=10)
label2.pack(pady=10)
text = tk.Text(root, height=5, width=50, wrap=tk.WORD, bg='#36393f', fg='#ffffff', font=("Arial", 10))
text.insert(tk.END, "Click the middle mouse button to switch modes \n there are two modes bankai and shikai however if you are using resurrection you would use the shikai mode and only the shikai mode")
text.pack(pady=10)

# Read hotkey from text file
read_hotkey()

# Set up the middle mouse button listener
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# Initialize hotkey listeners upon script startup
initialize_hotkey()

# Start Tkinter main loop
root.mainloop()
