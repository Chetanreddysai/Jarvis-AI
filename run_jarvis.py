"""
JARVIS Desktop Application Launcher
Starts the JARVIS server and launches the holographic interface in borderless App mode.
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
    Attempts to launch in dedicated standalone App Mode via Edge or Chrome,
    giving a 100% native desktop app experience without browser address bars.
    """
    time.sleep(1.2)  # Give server a moment to bind

    profile_dir = PROJECT_ROOT / "browser_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)

    # 1. Check Microsoft Edge (installed by default on Windows 10 & 11)
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge")
    ]
    for p in edge_paths:
        if p and os.path.exists(p):
            cmd = f'"{p}" --app="{url}" --user-data-dir="{profile_dir}" --start-maximized'
            print(f"[JARVIS Launch] Opening dedicated App Window via Edge: {cmd}")
            res = subprocess.Popen(cmd, shell=True)
            return

    # 2. Check Google Chrome
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        shutil.which("chrome")
    ]
    for p in chrome_paths:
        if p and os.path.exists(p):
            cmd = f'"{p}" --app="{url}" --user-data-dir="{profile_dir}" --start-maximized'
            print(f"[JARVIS Launch] Opening dedicated App Window via Chrome: {cmd}")
            subprocess.Popen(cmd, shell=True)
            return

    # 3. Fallback to default browser
    print("[JARVIS Launch] Opening in default web browser...")
    subprocess.Popen(f'start {url}', shell=True)

if __name__ == "__main__":
    print("=" * 60)
    print("   J.A.R.V.I.S. // STARK INDUSTRIES MARK VII ACTIVATION")
    print("   Voice-Controlled Autonomous System Interface")
    print("=" * 60)
    print("Initializing Core Protocols on http://127.0.0.1:5000 ...")

    # Start Flask server thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Launch desktop window
    launch_app_window()

    print("\n[JARVIS STATUS]: ONLINE AND LISTENING.")
    print("Press Ctrl+C in this terminal to power down JARVIS.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[JARVIS]: Powering down. Goodbye, sir.")
