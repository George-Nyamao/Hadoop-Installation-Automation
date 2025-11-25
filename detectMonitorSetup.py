import pyautogui

def check_monitor_setup():
    # Get primary screen size
    primary_width = pyautogui.size().width
    primary_height = pyautogui.size().height
    
    print(f"Primary Screen: {primary_width}x{primary_height}")
    print(f"Mouse Position: {pyautogui.position()}")
    
    # Get all windows and their positions
    windows = pyautogui.getAllWindows()
    print("\nFirst 10 windows and their positions:")
    for i, window in enumerate(windows[:10]):
        if window.title:  # Only show windows with titles
            print(f"{i+1}. '{window.title[:50]}...' - Position: ({window.left}, {window.top})")

check_monitor_setup()