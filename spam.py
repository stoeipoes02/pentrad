import pyautogui
import time

words = ['river','transfer', 'skyscraper', 'commercial', 'food', 'elementary school','tree','pen', 'roof', 'church', 'clothes', 'bird', 'telephone']

time.sleep(3)
location = pyautogui.position()

for i in range(len(words)):
    pyautogui.click(location)
    pyautogui.typewrite(words[i])
    pyautogui.press("enter")
    for i in range(len(words[i])):
        pyautogui.click(location)
        pyautogui.press("backspace")
    time.sleep(1)