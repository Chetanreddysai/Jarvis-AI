"""
JARVIS Central Web Server & Application Host
Powers the Iron Man HUD, handles real-time voice command processing,
audio synthesis streaming, and telemetry updates.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

import system_controller
import voice_engine
import jarvis_brain
import time
import threading
import speech_recognition as sr

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

brain = jarvis_brain.JarvisBrain()

# System state: ONLINE (True) vs STANDBY (False)
APP_STATE = {
    "is_active": True,
    "last_command": "",
    "last_response": "Standing by, sir.",
    "is_speaking": False
}

LAST_COMMAND = {"text": "", "time": 0.0}

def is_duplicate_command(text: str) -> bool:
    now = time.time()
    clean = text.lower().strip()
    if clean == LAST_COMMAND["text"] and (now - LAST_COMMAND["time"]) < 3.0:
        return True
    LAST_COMMAND["text"] = clean
    LAST_COMMAND["time"] = now
    return False

def start_native_microphone_worker():
    """
    Listens directly to the Windows microphone hardware in the background,
    ensuring voice commands work even if browser microphone permission is blocked.
    """
    def listen_loop():
        try:
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.7
            mic = sr.Microphone()
        except Exception as e:
            print(f"[JARVIS Native Mic Notice]: {e}")
            return

        print("[JARVIS Background Mic]: Hardware listener active and ready.")
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source, duration=0.6)
            except Exception:
                pass
            while True:
                if not APP_STATE.get("is_active", True):
                    time.sleep(1)
                    continue
                try:
                    audio = r.listen(source, timeout=4, phrase_time_limit=8)
                    raw_text = r.recognize_google(audio).strip()
                    if raw_text and not is_duplicate_command(raw_text):
                        lower = raw_text.lower()
                        print(f"[JARVIS Hardware Audio]: '{raw_text}'")
                        trigger_words = ["jarvis", "open", "volume", "play", "screenshot", "status", "mute", "close", "minimize", "power", "exit", "shutdown", "time", "date"]
                        if any(w in lower for w in trigger_words):
                            APP_STATE["last_command"] = raw_text
                            result = brain.process_command(raw_text)
                            speech = result.get("speech", "")
                            APP_STATE["last_response"] = speech
                            voice_engine.synthesize_speech(speech)
                            voice_engine.speak_direct(speech)
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except Exception:
                    time.sleep(0.5)

    threading.Thread(target=listen_loop, daemon=True).start()

start_native_microphone_worker()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "status": "online" if APP_STATE["is_active"] else "standby",
        "is_active": APP_STATE["is_active"],
        "last_command": APP_STATE["last_command"],
        "last_response": APP_STATE["last_response"],
        "is_speaking": APP_STATE["is_speaking"]
    })

@app.route("/api/toggle_state", methods=["POST"])
def toggle_state():
    data = request.get_json(silent=True) or {}
    new_state = data.get("is_active")
    if new_state is not None:
        APP_STATE["is_active"] = bool(new_state)
    else:
        APP_STATE["is_active"] = not APP_STATE["is_active"]
        
    state_str = "ONLINE" if APP_STATE["is_active"] else "STANDBY"
    msg = "All systems energized. Online and listening, sir." if APP_STATE["is_active"] else "Entering standby power mode. Systems asleep."
    
    # Generate voice greeting
    audio_path = voice_engine.synthesize_speech(msg)
    audio_rel = f"/api/audio?file={os.path.basename(audio_path)}" if audio_path else ""
    
    return jsonify({
        "success": True,
        "is_active": APP_STATE["is_active"],
        "state_text": state_str,
        "speech": msg,
        "audio_url": audio_rel
    })

@app.route("/api/telemetry", methods=["GET"])
def telemetry():
    stats = system_controller.get_system_telemetry()
    return jsonify(stats)

@app.route("/api/command", methods=["POST"])
def execute_command():
    if not APP_STATE["is_active"]:
        return jsonify({
            "success": False,
            "action": "standby_ignored",
            "speech": "JARVIS is currently in standby mode. Please power on the Arc Reactor.",
            "audio_url": ""
        }), 400

    data = request.get_json(silent=True) or {}
    command_text = data.get("text", "").strip()
    if not command_text:
        return jsonify({"success": False, "speech": "No command detected."})

    if is_duplicate_command(command_text):
        return jsonify({
            "success": True,
            "action": "duplicate_suppressed",
            "command": command_text,
            "speech": APP_STATE["last_response"],
            "audio_url": ""
        })

    APP_STATE["last_command"] = command_text
    
    # Process through Jarvis Brain
    result = brain.process_command(command_text)
    speech_text = result.get("speech", "Command executed, sir.")
    APP_STATE["last_response"] = speech_text
    
    # Synthesize British Jarvis Voice
    audio_file = voice_engine.synthesize_speech(speech_text)
    audio_url = ""
    if audio_file:
        audio_url = f"/api/audio?file={os.path.basename(audio_file)}"

    # Handle Shutdown or Standby Actions
    action = result.get("action", "unknown")
    if action == "shutdown_jarvis":
        def kill_process():
            time.sleep(3.5)
            os._exit(0)
        threading.Thread(target=kill_process, daemon=True).start()

    elif action == "standby_jarvis":
        APP_STATE["is_active"] = False

    return jsonify({
        "success": result.get("success", True),
        "action": result.get("action", "unknown"),
        "command": command_text,
        "speech": speech_text,
        "audio_url": audio_url,
        "details": result.get("details")
    })

@app.route("/api/audio", methods=["GET"])
def get_audio():
    filename = request.args.get("file", "")
    if not filename:
        return "Missing file parameter", 400
    
    # Sanitize filename
    clean_name = os.path.basename(filename)
    audio_file = voice_engine.CACHE_DIR / clean_name
    if audio_file.exists():
        mime = "audio/mpeg" if clean_name.endswith(".mp3") else "audio/wav"
        return send_file(str(audio_file), mimetype=mime)
    return "Audio file not found", 404

@app.route("/api/settings", methods=["GET", "POST"])
def handle_settings():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        updated = jarvis_brain.save_config(payload)
        brain.reload_config()
        return jsonify({"success": True, "settings": updated})
    return jsonify({"success": True, "settings": jarvis_brain.load_config()})

@app.route("/screenshots/<path:filename>")
def get_screenshot(filename):
    clean_name = os.path.basename(filename)
    shot_path = system_controller.SCREENSHOTS_DIR / clean_name
    if shot_path.exists():
        return send_file(str(shot_path), mimetype="image/png")
    return "Not found", 404

if __name__ == "__main__":
    port = 5000
    print(f"[JARVIS Server] Initializing on http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
