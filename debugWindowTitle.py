# Run this to see what your Medium article window title actually is
def debug_window_titles():
    import pyautogui
    print("=== CURRENT CHROME WINDOWS ===")
    windows = pyautogui.getWindowsWithTitle("Chrome")
    for i, win in enumerate(windows):
        print(f"{i+1}. '{win.title}'")
    print("==============================")

debug_window_titles()