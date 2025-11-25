import subprocess
import time
import pyautogui

def open_new_chrome_window_screen1():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Move mouse to Screen 1 first
    pyautogui.moveTo(100, 100)
    time.sleep(0.5)
    
    # Open NEW window (--new-window forces a separate window)
    subprocess.Popen([
        chrome_path,
        "--new-window",  # Forces a new window
        "https://medium.com/@gmnyamao/how-to-install-hadoop-on-windows-10-11-a-step-by-step-guide-7aa42d2df848"
    ])
    
    time.sleep(4)
    
    # Find the NEWEST Chrome window and maximize it on Screen 1
    chrome_windows = pyautogui.getWindowsWithTitle("Chrome")
    if chrome_windows:
        # Get the most recently active Chrome window (likely our new one)
        newest_chrome = chrome_windows[0]
        newest_chrome.maximize()
        print("✅ New Chrome window opened on Screen 1!")

open_new_chrome_window_screen1()