"""
J.A.R.V.I.S. Native Desktop GUI Application
Launches JARVIS directly into a dedicated, sleek native desktop window via WebView2.
Zero Command Prompt. Zero browser bars. 100% native Iron Man interface.
"""

import sys
import time
import threading
from pathlib import Path
import webview

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from app import app

def start_server():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1.0)

    # Create native Windows GUI window
    window = webview.create_window(
        title="J.A.R.V.I.S. // STARK INDUSTRIES MARK VII",
        url="http://127.0.0.1:5000",
        width=1280,
        height=820,
        resizable=True,
        min_size=(1000, 650),
        background_color="#03080e"
    )

    # Start the desktop window (zero console required)
    webview.start(gui="edgechromium", debug=False)
