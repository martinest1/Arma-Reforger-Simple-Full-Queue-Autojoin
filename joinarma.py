import time
import ctypes
import keyboard
from PIL import ImageGrab

INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("mi", MOUSEINPUT)]

def send_click():
    inp_down = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dwFlags=MOUSEEVENTF_LEFTDOWN))
    inp_up   = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(dwFlags=MOUSEEVENTF_LEFTUP))
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
    time.sleep(0.05)
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp_up), ctypes.sizeof(INPUT))

def color_in_range(c1, c2, tolerance=3):
    return all(abs(a - b) <= tolerance for a, b in zip(c1, c2))

def get_pixel_color(x, y):
    return ImageGrab.grab().getpixel((x, y))

running = False
TARGET_COLOR = (249, 66, 66)
CHECK_POS = (580, 439)

def start():
    global running
    running = True
    print("Started.")

def stop():
    global running
    running = False
    print("Stopped.")

keyboard.add_hotkey("f6", start)
keyboard.add_hotkey("f4", stop)

print("F6 = Start | F4 = Stop")

while True:
    if running:
        # Click
        send_click()
        time.sleep(0.5)

        # Check color
        color = get_pixel_color(CHECK_POS[0], CHECK_POS[1])
        if not color_in_range(color, TARGET_COLOR):
            print(f"Color mismatch: {color} — stopping.")
            running = False
            continue

        # Hold ESC for 2 seconds
        keyboard.press("esc")
        time.sleep(2)
        keyboard.release("esc")

        time.sleep(0.5)
    else:
        time.sleep(0.1)