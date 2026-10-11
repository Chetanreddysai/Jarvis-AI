"""
SAMPAN Desktop Application Launcher
Starts the SAMPAN server, ensures microphone permissions, and launches the holographic interface in borderless App mode.
"""

import os
import sys
import time
import json
import shutil
import threading
import subprocess
import webbrowser
from pathlib import Path
import psutil

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from app import app

def cleanup_previous_instances():
    """Frees port 5000 and kills any stale backend processes before starting."""
    current_pid = os.getpid()
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == 5000 and conn.pid and conn.pid != current_pid:
                try:
                    p = psutil.Process(conn.pid)
                    p.kill()
                    print(f"[SAMPAN Init] Freed port 5000 from old process (PID: {conn.pid})")
                except Exception:
                    pass
    except Exception:
        pass

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            name = (proc.info['name'] or '').lower()
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            if 'python' in name and ('run_sampan' in cmdline or 'app.py' in cmdline) and 'test_' not in cmdline:
                proc.kill()
                print(f"[SAMPAN Init] Cleaned old SAMPAN process (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def ensure_microphone_permissions(profile_dir: Path):
    """
    Pre-configures Chromium Preferences inside the profile directory
    to ensure microphone permission is always explicitly GRANTED (setting: 1)
    for http://127.0.0.1:5000.
    """
    default_dir = profile_dir / "Default"
    default_dir.mkdir(parents=True, exist_ok=True)
    pref_path = default_dir / "Preferences"

    try:
        data = {}
        if pref_path.exists():
            with open(pref_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        if "profile" not in data:
            data["profile"] = {}
        if "content_settings" not in data["profile"]:
            data["profile"]["content_settings"] = {}
        if "exceptions" not in data["profile"]["content_settings"]:
            data["profile"]["content_settings"]["exceptions"] = {}
        
        exc = data["profile"]["content_settings"]["exceptions"]
        exc["media_stream_mic"] = {
            "http://127.0.0.1:5000,*": {"setting": 1},
            "http://localhost:5000,*": {"setting": 1}
        }
        exc["sound"] = {
            "http://127.0.0.1:5000,*": {"setting": 1},
            "http://localhost:5000,*": {"setting": 1}
        }
        
        with open(pref_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("[SAMPAN Init] Microphone access pre-granted in browser profile.")
    except Exception as e:
        print(f"[SAMPAN Init Notice] Could not write preferences: {e}")

def start_server():
    """Runs the Flask backend."""
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def launch_app_window(url="http://127.0.0.1:5000"):
    """
    Launches in dedicated standalone App Mode via Edge or Chrome,
    giving a 100% native desktop app experience with microphone auto-granted.
    """
    time.sleep(1.0)

    profile_dir = PROJECT_ROOT / "browser_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    ensure_microphone_permissions(profile_dir)

    flags = [
        f'--app={url}',
        f'--user-data-dir={profile_dir}',
        '--use-fake-ui-for-media-stream',
        f'--unsafely-treat-insecure-origin-as-secure={url}',
        '--autoplay-policy=no-user-gesture-required',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-features=Translate,EdgeSidebar',
        '--enable-features=SpeechRecognition',
        '--start-maximized'
    ]

    # Candidate browsers
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        shutil.which("chrome")
    ]

    browser_bin = None
    for p in candidates:
        if p and os.path.exists(p):
            browser_bin = p
            break

    if browser_bin:
        cmd = [browser_bin] + flags
        print(f"[SAMPAN Launch] Launching interface via: {browser_bin}")
        proc = subprocess.Popen(cmd)
        
        # Monitor browser window lifecycle in a background watchdog thread
        def monitor_lifecycle():
            time.sleep(4.0)
            while True:
                time.sleep(2.0)
                still_running = False
                for p in psutil.process_iter(['name', 'cmdline']):
                    try:
                        name = (p.info['name'] or '').lower()
                        cmdline = ' '.join(p.info['cmdline'] or []).lower()
                        if ('msedge' in name or 'chrome' in name) and str(profile_dir).lower() in cmdline:
                            still_running = True
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                if not still_running:
                    print("\n[SAMPAN] UI window closed by user. Powering down background processes...")
                    os._exit(0)

        watchdog = threading.Thread(target=monitor_lifecycle, daemon=True)
        watchdog.start()
    else:
        print("[SAMPAN Launch] Opening in default web browser...")
        webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 60)
    print("   S.A.M.P.A.N. // AUTONOMOUS AI SYSTEM ACTIVATION")
    print("   Voice-Controlled Companion & System Interface")
    print("=" * 60)

    cleanup_previous_instances()

    print("Initializing Core Server on http://127.0.0.1:5000 ...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Launch UI
    launch_app_window()

    print("\n[SAMPAN STATUS]: ONLINE AND LISTENING.")
    print("Say 'Sampan' followed by your command or chat.")
    print("To stop, close the interface window or double-click STOP SAMPAN.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SAMPAN]: Powering down. Goodbye!")
        os._exit(0)
