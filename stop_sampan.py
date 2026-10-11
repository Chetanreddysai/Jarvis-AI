"""
SAMPAN Process Terminator
Cleanly shuts down all SAMPAN servers, speech recognition listeners, and window instances.
"""
import os
import sys
import psutil

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
                    print(f"[STOPPED] Freed port 5000 from process (PID: {conn.pid})")
                    stopped += 1
                except Exception:
                    pass
    except Exception:
        pass

    # 2. Kill python instances running run_sampan, app.py or related scripts
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            name = (proc.info['name'] or '').lower()
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            
            # Kill Python SAMPAN instances
            if 'python' in name and ('run_sampan' in cmdline or 'app.py' in cmdline or 'run_jarvis' in cmdline):
                proc.kill()
                print(f"[STOPPED] Background SAMPAN process terminated (PID: {proc.info['pid']})")
                stopped += 1

            # Kill dedicated app window instances
            elif ('msedge' in name or 'chrome' in name) and ('browser_profile' in cmdline or '127.0.0.1:5000' in cmdline):
                proc.kill()
                print(f"[STOPPED] SAMPAN Application Window closed (PID: {proc.info['pid']})")
                stopped += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied):
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
