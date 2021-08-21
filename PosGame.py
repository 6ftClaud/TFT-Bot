"""
Uncomment one of the HWNDs in WindowInfo function to find positions in Client or Game
"""
import pyautogui
import win32gui
from time import sleep


def WindowInfo():
    try:
        # Client
        hwnd = win32gui.FindWindow(None, "League of Legends")
        # Game
        #hwnd = win32gui.FindWindow(None, "League of Legends (TM) Client")
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        return (x, y)
    except:
        print("Either you haven't launched the game or the wrong hwnd is uncommented.")


try:
    print("Press Ctrl-C to quit")
    while True:
        sleep(0.1)
        offset = WindowInfo()
        x, y = pyautogui.position()
        rgb = pyautogui.pixel(x, y)
        x -= offset[0]
        y -= offset[1]
        print(f"X: {x} Y: {y}\tRGB: {rgb}")
except KeyboardInterrupt:
    print("\n")
