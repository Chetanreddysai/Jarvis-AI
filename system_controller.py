"""
SAMPAN System Controller - Hardware, OS & Window Control for Windows
Executes voice-activated commands to manage apps, audio, displays, power, and telemetry.
"""

import os
import sys
import re
import time
import ctypes
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
import psutil

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Windows Virtual Key Codes for Media & Volume
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT = 0xB0
VK_MEDIA_PREV = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

# Common Windows App mappings
APP_REGISTRY = {
    "chrome": "start chrome",
    "google chrome": "start chrome",
    "edge": "start msedge",
    "microsoft edge": "start msedge",
    "browser": "start msedge",
    "notepad": "notepad",
    "notepad++": "start notepad++",
    "calculator": "calc",
    "calc": "calc",
    "terminal": "start wt",
    "cmd": "start cmd",
    "command prompt": "start cmd",
    "powershell": "start powershell",
    "file explorer": "explorer",
    "explorer": "explorer",
    "task manager": "taskmgr",
    "settings": "start ms-settings:",
    "control panel": "control",
    "camera": "start microsoft.windows.camera:",
    "vscode": "code",
    "visual studio code": "code",
    "code": "code",
    "spotify": "start spotify:",
    "paint": "mspaint",
    "word": "start winword",
    "microsoft word": "start winword",
    "ms word": "start winword",
    "winword": "start winword",
    "excel": "start excel",
    "microsoft excel": "start excel",
    "ms excel": "start excel",
    "powerpoint": "start powerpnt",
    "microsoft powerpoint": "start powerpnt",
    "teams": "start msteams:",
    "microsoft teams": "start msteams:",
    "ms teams": "start msteams:",
    "whatsapp": "start whatsapp:",
    "discord": "start discord:",
    "downloads": "explorer shell:Downloads",
    "documents": "explorer shell:Personal",
    "desktop": "explorer shell:Desktop"
}

# Recognized Web Services & Cloud Apps
WEB_SERVICES = {
    "teams": "https://teams.microsoft.com",
    "microsoft teams": "https://teams.microsoft.com",
    "ms teams": "https://teams.microsoft.com",
    "gmail": "https://mail.google.com",
    "email": "https://mail.google.com",
    "mail": "https://mail.google.com",
    "youtube": "https://www.youtube.com",
    "whatsapp": "https://web.whatsapp.com",
    "whatsapp web": "https://web.whatsapp.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "google": "https://www.google.com",
    "maps": "https://maps.google.com",
    "google maps": "https://maps.google.com",
    "drive": "https://drive.google.com",
    "google drive": "https://drive.google.com",
    "calendar": "https://calendar.google.com",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://x.com",
    "x": "https://x.com",
    "instagram": "https://www.instagram.com",
    "netflix": "https://www.netflix.com",
    "reddit": "https://www.reddit.com",
    "amazon": "https://www.amazon.in"
}

def _send_key_event(vk_code):
    """Simulates a single hardware key press and release."""
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)

# ================= AUDIO & MEDIA =================

def volume_up(steps=5):
    """Increases master volume."""
    for _ in range(steps):
        _send_key_event(VK_VOLUME_UP)
    return f"Increased volume by {steps * 2}%"

def volume_down(steps=5):
    """Decreases master volume."""
    for _ in range(steps):
        _send_key_event(VK_VOLUME_DOWN)
    return f"Decreased volume by {steps * 2}%"

def volume_mute():
    """Toggles audio mute."""
    _send_key_event(VK_VOLUME_MUTE)
    return "Toggled audio mute"

def media_play_pause():
    """Plays or pauses current media."""
    _send_key_event(VK_MEDIA_PLAY_PAUSE)
    return "Toggled media playback"

def media_next():
    """Skips to next media track."""
    _send_key_event(VK_MEDIA_NEXT)
    return "Skipped to next track"

def media_previous():
    """Goes to previous media track."""
    _send_key_event(VK_MEDIA_PREV)
    return "Returned to previous track"

# ================= APPLICATION & WEB MANAGEMENT =================

def open_web_service_in_browser(service_name: str, browser: str = "chrome") -> tuple[bool, str]:
    """Launches a specific web service or site in a designated browser."""
    clean_svc = service_name.lower().strip()
    clean_browser = browser.lower().strip()

    # Determine browser CLI launcher
    if "edge" in clean_browser:
        browser_cmd = "start msedge"
    elif "chrome" in clean_browser:
        browser_cmd = "start chrome"
    else:
        browser_cmd = "start"

    # Resolve URL
    url = WEB_SERVICES.get(clean_svc)
    if not url:
        if clean_svc.startswith("http://") or clean_svc.startswith("https://"):
            url = clean_svc
        elif "." in clean_svc and not " " in clean_svc:
            url = f"https://{clean_svc}"
        else:
            url = f"https://www.google.com/search?q={clean_svc}"

    try:
        subprocess.Popen(f"{browser_cmd} \"{url}\"", shell=True)
        return True, f"Opening {service_name} in {clean_browser}."
    except Exception as e:
        return False, f"Failed to open {service_name} in {clean_browser}: {e}"

def open_application(app_name: str) -> tuple[bool, str]:
    """Launches an application by name or recognized alias."""
    clean_name = app_name.lower().strip()

    # Direct alias match in APP_REGISTRY
    if clean_name in APP_REGISTRY:
        cmd = APP_REGISTRY[clean_name]
        try:
            subprocess.Popen(cmd, shell=True)
            return True, f"Launching {app_name} for you."
        except Exception as e:
            return False, f"Failed to launch {app_name}: {e}"

    # Check WEB_SERVICES (e.g. "open teams", "open gmail")
    if clean_name in WEB_SERVICES:
        url = WEB_SERVICES[clean_name]
        try:
            subprocess.Popen(f"start \"\" \"{url}\"", shell=True)
            return True, f"Opening {app_name} in your browser."
        except Exception:
            pass

    # Partial search in registry (whole word priority)
    for key, cmd in APP_REGISTRY.items():
        if key == clean_name or re.search(r'\b' + re.escape(key) + r'\b', clean_name):
            try:
                subprocess.Popen(cmd, shell=True)
                return True, f"Opening {key} for you."
            except Exception as e:
                return False, f"Error opening {key}: {e}"

    # Fallback: attempt to start generic process or URL
    try:
        subprocess.Popen(f"start \"\" {clean_name}", shell=True)
        return True, f"Attempting to launch {app_name}."
    except Exception as e:
        return False, f"Could not locate an application named {app_name}."

def type_text_into_window(text: str) -> bool:
    """Simulates typing text directly into the currently focused window."""
    try:
        import pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.write(text, interval=0.03)
        return True
    except Exception as e:
        print(f"[Typing Error]: {e}")
        return False

def close_application(app_name: str) -> tuple[bool, str]:
    """Terminates running processes matching the name."""
    clean_name = app_name.lower().strip()
    # Map common aliases to executable names
    exe_map = {
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "code": "Code.exe",
        "vscode": "Code.exe",
        "spotify": "Spotify.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "paint": "mspaint.exe"
    }

    target_proc = exe_map.get(clean_name, f"{clean_name}.exe")
    killed = False
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if clean_name in proc.info['name'].lower() or proc.info['name'].lower() == target_proc.lower():
                proc.terminate()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed:
        return True, f"Closed {app_name}, sir."
    else:
        # Try taskkill as backup
        res = subprocess.run(f"taskkill /F /IM {target_proc}", shell=True, capture_output=True)
        if res.returncode == 0:
            return True, f"Terminated {app_name}."
        return False, f"No active process found for {app_name}."

# ================= OS & WINDOWS AUTOMATION =================

def minimize_all_windows():
    """Minimizes all windows to reveal desktop (Win+D)."""
    # Key combination: Win (0x5B) + D (0x44)
    VK_LWIN = 0x5B
    ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)
    ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
    return "Minimizing all active windows, sir."

def lock_screen():
    """Instantly locks the Windows workstation."""
    ctypes.windll.user32.LockWorkStation()
    return "Securing workstation. Screen locked."

def take_screenshot() -> tuple[bool, str, str]:
    """Captures the primary monitor and saves to screenshots folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = SCREENSHOTS_DIR / f"sampan_screenshot_{timestamp}.png"
    
    # Try PIL / pyautogui
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        img.save(str(filepath))
        return True, str(filepath), f"Screenshot captured and stored."
    except Exception as e:
        # Fallback to powershell screenshot
        ps_cmd = (
            f"[Reflection.Assembly]::LoadWithPartialName('System.Drawing') | Out-Null; "
            f"[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; "
            f"$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
            f"$bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height; "
            f"$graphics = [Drawing.Graphics]::FromImage($bmp); "
            f"$graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size); "
            f"$bmp.Save('{filepath}'); "
            f"$graphics.Dispose(); $bmp.Dispose()"
        )
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
            return True, str(filepath), f"Screenshot captured successfully."
        except Exception as ps_err:
            return False, "", f"Unable to capture screenshot: {ps_err}"

# ================= WEB & SEARCH =================

def search_google(query: str):
    """Opens browser with Google search."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for '{query}', sir."

def play_youtube(query: str):
    """Searches YouTube and opens relevant video."""
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return f"Playing '{query}' on YouTube now."

def open_url(url: str):
    """Opens a website URL."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Navigating to {url}."

# ================= SYSTEM TELEMETRY =================

def get_system_telemetry() -> dict:
    """Returns real-time CPU, RAM, Battery, and Disk diagnostics."""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count(logical=True)
    
    mem = psutil.virtual_memory()
    ram_percent = mem.percent
    ram_used_gb = round(mem.used / (1024**3), 2)
    ram_total_gb = round(mem.total / (1024**3), 2)
    
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_free_gb = round(disk.free / (1024**3), 2)
    
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else 100
    is_plugged = battery.power_plugged if battery else True
    
    # Current time
    now = datetime.now()
    current_time_str = now.strftime("%I:%M %p")
    current_date_str = now.strftime("%A, %B %d, %Y")

    return {
        "cpu_percent": cpu_percent,
        "cpu_count": cpu_count,
        "ram_percent": ram_percent,
        "ram_used_gb": ram_used_gb,
        "ram_total_gb": ram_total_gb,
        "disk_percent": disk_percent,
        "disk_free_gb": disk_free_gb,
        "battery_percent": battery_percent,
        "battery_charging": is_plugged,
        "time": current_time_str,
        "date": current_date_str,
        "status": "ALL SYSTEMS NOMINAL"
    }

def get_system_report() -> str:
    """Creates a natural-sounding SAMPAN status briefing."""
    data = get_system_telemetry()
    status_brief = (
        f"All systems are operational, my friend. "
        f"CPU load is currently at {data['cpu_percent']} percent, "
        f"Memory utilization is at {data['ram_percent']} percent ({data['ram_used_gb']} of {data['ram_total_gb']} gigabytes). "
    )
    if data['battery_percent'] is not None and data['battery_percent'] < 100:
        status_brief += f"Power levels are at {data['battery_percent']} percent{' and charging' if data['battery_charging'] else ''}. "
    status_brief += f"The time is {data['time']}."
    return status_brief
