
import pyautogui
import keyboard
import win32gui
import time

# Replace with the title of the application you want it to work in
TARGET_WINDOW_TITLE = "Your Application Title"


def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)


def autoclick():
    while True:
        # Check if the target window is active
        if get_active_window_title() == TARGET_WINDOW_TITLE:
            # If left mouse button is held down, click
            if pyautogui.mouseDown(button="left"):
                pyautogui.click()
                time.sleep(0.05)  # Adjust for click speed
        else:
            time.sleep(0.5)  # Check less frequently when not in the target app

        # Exit the script when 'esc' is pressed
        if keyboard.is_pressed('esc'):
            print("Exiting autoclicker...")
            break


if __name__ == "__main__":
    print("Press 'esc' to exit the autoclicker.")
    autoclick()
