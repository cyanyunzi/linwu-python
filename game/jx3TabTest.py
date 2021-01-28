import pyautogui as pyautogui
import time

count = 1;
while True:
    pyautogui.hotkey('command', 'tab')
    count = count +1;
    time.sleep(1)
    if (count % 2)==0:
        pyautogui.typewrite('monijiansanmoyu')
        pyautogui.typewrite('dingshiqiehuanchuangkou')
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
    if count == 10:
        pyautogui.typewrite('jiaobenzhixingwanbi')
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        break;