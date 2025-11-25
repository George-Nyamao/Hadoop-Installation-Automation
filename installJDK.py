import os
import shutil
import subprocess
import tempfile
import time
import pyautogui


def load_env_from_file(env_path=".env"):
    """Lightweight .env loader to bring ORACLE credentials into the environment."""
    if not os.path.exists(env_path):
        print(f"WARN: {env_path} not found; expecting ORACLE_USERNAME/ORACLE_PASSWORD to be set in environment.")
        return

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value and key not in os.environ:
                    os.environ[key] = value
        print(f"OK: Loaded environment variables from {env_path}")
    except Exception as e:
        print(f"WARN: Could not load {env_path}: {e}")


def clear_recent_chrome_cache(profile_root, minutes=60):
    """Best-effort cache purge for the last N minutes in the given Chrome profile root."""
    cutoff = time.time() - (minutes * 60)
    targets = [
        os.path.join(profile_root, "Default", "Cache"),
        os.path.join(profile_root, "Default", "Code Cache"),
        os.path.join(profile_root, "Default", "GPUCache"),
        os.path.join(profile_root, "Default", "Network"),
    ]

    removed = 0
    for target in targets:
        if not os.path.exists(target):
            continue
        for root, dirs, files in os.walk(target):
            for name in files:
                path = os.path.join(root, name)
                try:
                    if os.path.getmtime(path) >= cutoff:
                        os.remove(path)
                        removed += 1
                except Exception:
                    pass
            # Optionally prune empty dirs
            for d in list(dirs):
                dir_path = os.path.join(root, d)
                try:
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                except Exception:
                    pass
    print(f"OK: Cleared ~{removed} recent cache files (last {minutes} minutes).")


def open_chrome_with_medium_article():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    medium_article = "https://medium.com/@gmnyamao/how-to-install-hadoop-on-windows-10-11-a-step-by-step-guide-7aa42d2df848"
    # Dedicated temp profile with normal tabs so links stay in this window, isolated from your main profile
    automation_profile = os.path.join(tempfile.gettempdir(), "chrome_medium_profile")
    # Clear recent cache/cookies so the Oracle flow always shows the license dialog
    clear_recent_chrome_cache(automation_profile, minutes=60)
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
                                if click_oracle_download_link():
                                    print("Waiting for Oracle sign-in page to load...")
                                    time.sleep(6)
                                    if oracle_sign_in_username_step():
                                        time.sleep(3)
                                        if oracle_sign_in_password_step():
                                            time.sleep(3)
                                            wait_for_download_and_open_installer()
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


def oracle_sign_in_username_step():
    """On the Oracle sign-in page, type the username/email and click Next."""

    print("Attempting Oracle sign-in (username step)...")

    username = os.environ.get("ORACLE_USERNAME")
    if not username:
        print("WARN: ORACLE_USERNAME not set; add it to your environment or .env file.")
        return False

    try:
        # Focus should already be in the username field; type then click Next
        pyautogui.write(username, interval=0.05)
        time.sleep(0.5)

        next_location = pyautogui.locateOnScreen("oracle_signin_next_link.png", confidence=0.7)
        if next_location:
            next_center = pyautogui.center(next_location)
            pyautogui.moveTo(next_center, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            print("OK: Entered username and clicked Next.")
            return True
        else:
            print("WARN: Could not find Oracle sign-in Next button on screen.")
            return False

    except Exception as e:
        print(f"ERROR during Oracle sign-in username step: {e}")
        return False


def oracle_sign_in_password_step():
    """On the Oracle sign-in password page, type the password and click Sign In."""

    print("Attempting Oracle sign-in (password step)...")

    password = os.environ.get("ORACLE_PASSWORD")
    if not password:
        print("WARN: ORACLE_PASSWORD not set; add it to your environment or .env file.")
        return False

    try:
        # Focus should already be in the password field; type then click Sign In
        pyautogui.write(password, interval=0.05)
        time.sleep(0.5)

        signin_location = pyautogui.locateOnScreen("oracle_signin_signin_link.png", confidence=0.7)
        if signin_location:
            signin_center = pyautogui.center(signin_location)
            pyautogui.moveTo(signin_center, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            print("OK: Entered password and clicked Sign In.")
            return True
        else:
            print("WARN: Could not find Oracle Sign In button on screen.")
            return False

    except Exception as e:
        print(f"ERROR during Oracle sign-in password step: {e}")
        return False


def wait_for_download_and_open_installer(timeout_seconds=180):
    """Wait for the download to appear, then open the downloaded JDK installer from the Chrome downloads flyout."""

    print("Waiting for download to finish and appear in Chrome downloads...")
    start = time.time()
    downloads_icon = None

    while time.time() - start < timeout_seconds:
        downloads_icon = pyautogui.locateOnScreen("downloads_icon_link.png", confidence=0.7)
        if downloads_icon:
            break
        time.sleep(2)

    if not downloads_icon:
        print("WARN: Downloads icon not found within timeout.")
        return False

    try:
        downloads_center = pyautogui.center(downloads_icon)
        pyautogui.moveTo(downloads_center, duration=0.5)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(1.5)  # allow the downloads flyout to open

        exe_link = pyautogui.locateOnScreen("oracle_downloaded_jdk11_exe_link.png", confidence=0.7)
        if exe_link:
            exe_center = pyautogui.center(exe_link)
            pyautogui.moveTo(exe_center, duration=0.5)
            time.sleep(0.2)
            pyautogui.click()
            print("OK: Opened downloaded JDK installer from Chrome downloads.")
            return True
        else:
            print("WARN: Downloaded JDK exe link not found in downloads flyout.")
            return False

    except Exception as e:
        print(f"ERROR while opening downloaded JDK installer: {e}")
        return False


def verify_image_files():
    """Verify that required image files exist."""
    required_images = [
        "jdk_link.png",
        "jdk_windows_link.png",
        "jdk11_windows_exe_download_link.png",
        "oracle_agreement_checkbox.png",
        "download_jdk11_for_windows_link.png",
        "oracle_signin_next_link.png",
        "oracle_signin_signin_link.png",
        "downloads_icon_link.png",
        "oracle_downloaded_jdk11_exe_link.png",
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
    load_env_from_file()
    if verify_image_files():
        print("Starting automated Medium article navigation...")
        open_chrome_with_medium_article()
    else:
        print("Please ensure all required images are in the same folder as this script")
