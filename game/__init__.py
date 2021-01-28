import pyautogui as pyautogui
import time

while True :
    pyautogui.keyDown('n')
    time.sleep(1)
    pyautogui.keyUp('n')
    print("按下 n")