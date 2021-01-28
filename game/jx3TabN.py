import pyautogui as pyautogui
import time

while True:
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(1)
    pyautogui.keyDown('n')
    pyautogui.keyUp('n')
