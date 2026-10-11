import ctypes
import os
from time import sleep

# Define constants for the Windows MessageBox
MB_OK = 0x00000000
MB_ICONINFORMATION = 0x00000040

def show_expired_dialog():
    text = "Your trial has expired. Thank you for playig Freecraft 3D"
    title = "YourTrial Has Expiraed"
    sleep(120)
    ctypes.windll.user32.MessageBoxW(0, text, title, MB_OK | MB_ICONINFORMATION)
    os._exit(0)

