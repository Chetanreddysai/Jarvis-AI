"""
SAMPAN Desktop Application Launcher
Starts the SAMPAN server and launches the holographic interface in borderless App mode.
"""

import os
import sys
import time
import shutil
import threading
import subprocess
import webbrowser
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from app import app

def start_server():
    """Runs the Flask backend."""
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def launch_app_window(url="http://127.0.0.1:5000"):
    """
    Launches in dedicated standalone App Mode via Edge or Chrome,
    giving a 100% native desktop app experience without browser address bars.
    """
    time.sleep(1.2)

    profile_dir = PROJECT_ROOT / "browser_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)

    flags = (
        f'--app="{url}" '
        f'--user-data-dir="{profile_dir}" '
        '--use-fake-ui-for-media-stream '
        f'--unsafely-treat-insecure-origin-as-secure="{url}" '
        '--autoplay-policy=no-user-gesture-required '
        '--start-maximized'
    )

    # 1. Check Microsoft Edge (installed by default on Windows 10 & 11)
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge")
    ]
    for p in edge_paths:
        if p and os.path.exists(p):
            cmd = f'"{p}" {flags}'
            print(f"[SAMPAN Launch] Opening dedicated App Window via Edge: {cmd}")
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
            print("[SAMPAN] App window closed. Shutting down all processes...")
            os._exit(0)

    # 2. Check Google Chrome
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        shutil.which("chrome")
    ]
    for p in chrome_paths:
        if p and os.path.exists(p):
            cmd = f'"{p}" {flags}'
            print(f"[SAMPAN Launch] Opening dedicated App Window via Chrome: {cmd}")
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
            print("[SAMPAN] App window closed. Shutting down all processes...")
            os._exit(0)

    # 3. Fallback to default browser
    print("[SAMPAN Launch] Opening in default web browser...")
    subprocess.Popen(f'start {url}', shell=True)

if __name__ == "__main__":
    print("=" * 60)
    print("   S.A.M.P.A.N. // AUTONOMOUS AI SYSTEM ACTIVATION")
    print("   Voice-Controlled Companion & System Interface")
    print("=" * 60)
    print("Initializing Core Protocols on http://127.0.0.1:5000 ...")

    # Start Flask server thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Launch desktop window
    launch_app_window()

    print("\n[SAMPAN STATUS]: ONLINE AND LISTENING.")
    print("Press Ctrl+C in this terminal to power down SAMPAN.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SAMPAN]: Powering down. Goodbye!")
