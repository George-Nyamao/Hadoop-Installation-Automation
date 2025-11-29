"""
Capture the coordinates of the next left mouse click and print them.
Usage: run this script, click once anywhere; it will print (x, y) and exit.
"""

from pynput import mouse


def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print(f"Click at: ({x}, {y})")
        return False  # stop listener


if __name__ == "__main__":
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
