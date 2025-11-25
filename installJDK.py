import os
import subprocess
import tempfile
import time
import pyautogui


def open_chrome_with_medium_article():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    medium_article = "https://medium.com/@gmnyamao/how-to-install-hadoop-on-windows-10-11-a-step-by-step-guide-7aa42d2df848"
    # Dedicated temp profile with normal tabs so links stay in this window, isolated from your main profile
    automation_profile = os.path.join(tempfile.gettempdir(), "chrome_medium_profile")
    os.makedirs(automation_profile, exist_ok=True)

    print("Opening Chrome for screen recording...")

    try:
        # Track existing window handles so we can identify the new one reliably
        existing_handles = {w._hWnd for w in pyautogui.getAllWindows() if hasattr(w, "_hWnd")}

        pyautogui.moveTo(20, 20)
        time.sleep(0.5)

        subprocess.Popen([
            chrome_path,
            f"--user-data-dir={automation_profile}",
            "--profile-directory=Default",
            "--new-window",
            "--disable-extensions",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized",
            medium_article,
        ])

        # Wait for a new window handle to appear (up to ~8 seconds)
        target_window = None
        for _ in range(16):
            time.sleep(0.5)
            all_windows = pyautogui.getAllWindows()
            new_windows = [w for w in all_windows if hasattr(w, "_hWnd") and w._hWnd not in existing_handles]
            if new_windows:
                target_window = new_windows[0]
                break

        # Fallbacks if the new window detection missed
        if not target_window:
            medium_windows = [w for w in pyautogui.getAllWindows() if "Medium" in (w.title or "")]
            if medium_windows:
                target_window = medium_windows[0]
            else:
                chrome_windows = pyautogui.getWindowsWithTitle("Chrome")
                target_window = chrome_windows[0] if chrome_windows else pyautogui.getActiveWindow()

        if target_window:
            try:
                target_window.maximize()
            except Exception:
                pass
            try:
                target_window.activate()
            except Exception:
                pass
            print("OK: New Chrome window opened on Screen 1.")

            if scroll_to_step1_with_image():
                time.sleep(3)
                if click_jdk_download_link_with_image():
                    # Give the Oracle page a moment to load before looking for the Windows tab
                    time.sleep(5)
                    if click_windows_tab_with_image():
                        time.sleep(2)
                        if click_jdk11_windows_exe_with_image():
                            time.sleep(2)
                            if click_oracle_agreement_checkbox():
                                time.sleep(1)
                                click_oracle_download_link()
        else:
            print("WARN: Chrome opened but window not found.")

    except Exception as e:
        print(f"ERROR: {e}")


def scroll_to_step1_with_image():
    """Scroll to Step 1: Install Java and click on the Open JDK download page link."""

    print("Scrolling to Step 1 using image recognition...")

    try:
        pyautogui.click(100, 100)  # click to focus
        pyautogui.hotkey("ctrl", "home")  # Scroll to top
        time.sleep(2)

        # Faster/longer scan
        max_scroll_attempts = 120
        scroll_step = -80  # bigger jump per scroll
        pause_between_scrolls = 0.15

        for attempt in range(1, max_scroll_attempts + 1):
            try:
                link_location = pyautogui.locateOnScreen("jdk_link.png", confidence=0.7)
                if link_location:
                    print("OK: Found Step 1 area (JDK link detected)!")

                    pyautogui.scroll(5)  # small scroll up
                    time.sleep(1)

                    print("OK: Step 1 perfectly positioned for recording!")
                    return True

            except pyautogui.ImageNotFoundException:
                pass

            pyautogui.scroll(scroll_step)  # scroll down faster
            time.sleep(pause_between_scrolls)

            print(f"Scrolling... Attempt {attempt}/{max_scroll_attempts}")

        print("WARN: Could not find Step 1 area after maximum scroll attempts.")
        return False

    except Exception as e:
        print(f"ERROR during scrolling: {e}")
        return False


def click_jdk_download_link_with_image():
    """Click on the 'Open JDK download page' link using image recognition."""

    print("Looking for 'Open JDK download page' link...")

    try:
        link_location = pyautogui.locateOnScreen("jdk_link.png", confidence=0.7)

        if link_location:
            link_center = pyautogui.center(link_location)

            pyautogui.moveTo(link_center, duration=1)
            time.sleep(1)

            pyautogui.click()
            print("OK: Successfully clicked on Open JDK download page link!")

            time.sleep(3)
            return True
        else:
            print("WARN: JDK download link not found on screen.")
            return False

    except Exception as e:
        print(f"ERROR during clicking JDK link: {e}")
        return False


def click_windows_tab_with_image():
    """On the Oracle downloads page, click the Windows tab using image recognition."""

    print("Looking for Windows tab on Oracle JDK download page...")

    try:
        pyautogui.click(200, 200)  # focus the browser
        time.sleep(1)

        tab_location = pyautogui.locateOnScreen("jdk_windows_link.png", confidence=0.7)

        if tab_location:
            tab_center = pyautogui.center(tab_location)
            pyautogui.moveTo(tab_center, duration=1)
            time.sleep(0.5)
            pyautogui.click()
            print("OK: Windows tab clicked.")
            return True
        else:
            print("WARN: Windows tab image not found on screen.")
            return False

    except Exception as e:
        print(f"ERROR during clicking Windows tab: {e}")
        return False


def click_jdk11_windows_exe_with_image():
    """On the Windows tab, click the JDK 11.0.29 Windows x64 .exe download link using image recognition."""

    print("Looking for JDK 11 Windows x64 .exe download link...")

    try:
        pyautogui.click(200, 200)  # focus the browser
        time.sleep(1)

        link_location = pyautogui.locateOnScreen("jdk11_windows_exe_download_link.png", confidence=0.7)

        if link_location:
            link_center = pyautogui.center(link_location)
            pyautogui.moveTo(link_center, duration=1)
            time.sleep(0.5)
            pyautogui.click()
            print("OK: JDK 11 Windows x64 .exe link clicked.")
            return True
        else:
            print("WARN: JDK 11 Windows x64 .exe link image not found on screen.")
            return False

    except Exception as e:
        print(f"ERROR during clicking JDK 11 Windows .exe link: {e}")
        return False


def click_oracle_agreement_checkbox():
    """Click the Oracle license agreement checkbox in the download dialog."""

    print("Looking for Oracle license agreement checkbox...")

    try:
        checkbox_location = pyautogui.locateOnScreen("oracle_agreement_checkbox.png", confidence=0.7)

        if checkbox_location:
            checkbox_center = pyautogui.center(checkbox_location)
            pyautogui.moveTo(checkbox_center, duration=0.7)
            time.sleep(0.3)
            pyautogui.click()
            print("OK: Oracle license checkbox clicked.")
            return True
        else:
            print("WARN: Oracle license checkbox image not found on screen.")
            return False

    except Exception as e:
        print(f"ERROR during clicking Oracle license checkbox: {e}")
        return False


def click_oracle_download_link():
    """Click the download link inside the Oracle license dialog."""

    print("Looking for Oracle download link button...")

    try:
        download_location = pyautogui.locateOnScreen("download_jdk11_for_windows_link.png", confidence=0.7)

        if download_location:
            download_center = pyautogui.center(download_location)
            pyautogui.moveTo(download_center, duration=0.7)
            time.sleep(0.3)
            pyautogui.click()
            print("OK: Oracle download link clicked.")
            return True
        else:
            print("WARN: Oracle download link image not found on screen.")
            return False

    except Exception as e:
        print(f"ERROR during clicking Oracle download link: {e}")
        return False


def verify_image_files():
    """Verify that required image files exist."""
    required_images = [
        "jdk_link.png",
        "jdk_windows_link.png",
        "jdk11_windows_exe_download_link.png",
        "oracle_agreement_checkbox.png",
        "download_jdk11_for_windows_link.png",
    ]
    missing = []

    for image_name in required_images:
        if os.path.exists(image_name):
            file_size = os.path.getsize(image_name)
            print(f"OK: Found {image_name} ({file_size} bytes)")
        else:
            missing.append(image_name)
            print(f"WARN: {image_name} not found in current directory")

    if missing:
        print("Current directory:", os.getcwd())
        return False
    return True


if __name__ == "__main__":
    if verify_image_files():
        print("Starting automated Medium article navigation...")
        open_chrome_with_medium_article()
    else:
        print("Please ensure all required images are in the same folder as this script")
