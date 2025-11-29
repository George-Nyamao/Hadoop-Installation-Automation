import pyautogui
import time
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def activate_and_click():
    """Activate the Java installer window and click the Next button coordinates."""
    java_windows = pyautogui.getWindowsWithTitle("Java(TM) SE Development Kit")

    if not java_windows:
        print("Java installer window not found! Searching for any Java-related windows...")
        all_windows = pyautogui.getAllWindows()
        java_windows = [w for w in all_windows if "Java" in (w.title or "") or "JDK" in (w.title or "")]

    if not java_windows:
        print("No Java windows found. Please make sure the installer is open.")
        return False

    java_window = java_windows[0]
    print(f"Found window: '{java_window.title}'")

    try:
        print("Activating window...")
        java_window.activate()
    except Exception:
        pass
    time.sleep(2)

    active_window = pyautogui.getActiveWindow()
    if active_window and active_window.title == java_window.title:
        print("Window successfully activated!")
    else:
        print("Warning: Window may not be fully active")

    x, y = 1046, 687
    print(f"Clicking at coordinates: ({x}, {y})")
    pyautogui.moveTo(x, y, duration=1)
    pyautogui.click()
    print("Click executed!")
    return True


if __name__ == "__main__":
    if not is_admin():
        print("Restarting with admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("Running with admin privileges!")
    activate_and_click()
