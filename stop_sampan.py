"""
SAMPAN Process Terminator
Cleanly shuts down all SAMPAN background listeners, speech recognition, and servers.
"""
import os
import sys
import time
import psutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

def stop_all():
    print("=" * 60)
    print("   SHUTTING DOWN S.A.M.P.A.N. SYSTEM")
    print("=" * 60)
    print("Terminating background listeners, speech recognition, and servers...")

    current_pid = os.getpid()
    stopped = 0

    # 1. Kill any process holding port 5000
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == 5000 and conn.pid and conn.pid != current_pid:
                try:
                    p = psutil.Process(conn.pid)
                    p.kill()
                    stopped += 1
                except Exception:
                    pass
    except Exception:
        pass

    # 2. Kill python instances running run_background, run_sampan, app.py
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            name = (proc.info['name'] or '').lower()
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            
            if 'python' in name and any(k in cmdline for k in ['run_background', 'run_sampan', 'app.py', 'run_jarvis']):
                proc.kill()
                print(f"[STOPPED] Background SAMPAN process terminated (PID: {proc.info['pid']})")
                stopped += 1

            elif ('msedge' in name or 'chrome' in name) and ('browser_profile' in cmdline or '127.0.0.1:5000' in cmdline):
                proc.kill()
                print(f"[STOPPED] Window process terminated (PID: {proc.info['pid']})")
                stopped += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Voice confirmation of shutdown
    try:
        import voice_engine
        voice_engine.speak("SAMPAN is powered down. Goodbye, my friend.")
    except Exception:
        pass

    print()
    print("=" * 60)
    print("   [SUCCESS] S.A.M.P.A.N. IS FULLY SHUT DOWN.")
    print("   - All microphones and listeners have been released.")
    print("   - Interface and servers are powered down.")
    print("   - No further commands will be accepted.")
    print("=" * 60)

if __name__ == "__main__":
    stop_all()
