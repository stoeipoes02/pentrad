import pyautogui
import time

words = ['river','transfer', 'skyscraper', 'commercial', 'food', 'elementary school','tree','pen', 'roof', 'church', 'clothes', 'bird', 'telephone']

for i in range(len(words)):
    pyautogui.click(3028,158)
    pyautogui.typewrite(words[i])
    pyautogui.press("enter")
    for i in range(len(words[i])):
        pyautogui.click(3028,158)
        pyautogui.press("backspace")
    time.sleep(1)