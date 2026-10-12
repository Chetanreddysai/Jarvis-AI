"""
SAMPAN Background Voice Companion
Runs 100% in the background with NO browser window or webpage.
Listens to the laptop microphone, searches the internet for answers,
controls Windows, and speaks directly through the laptop speakers.
"""

import os
import sys
import time
import logging
from pathlib import Path
import psutil

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

import voice_engine
import sampan_brain

# Setup file logging for background operations
LOG_FILE = PROJECT_ROOT / "sampan_background.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def cleanup_previous_instances():
    """Kills any old SAMPAN background listeners before starting."""
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            name = (proc.info['name'] or '').lower()
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            if 'python' in name and ('run_background.py' in cmdline or 'run_sampan.py' in cmdline):
                proc.kill()
                logging.info(f"Killed old SAMPAN process: {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def main():
    cleanup_previous_instances()
    brain = sampan_brain.SampanBrain()
    
    logging.info("SAMPAN Background Voice Companion starting up...")
    print("=" * 60)
    print("   S.A.M.P.A.N. // BACKGROUND VOICE ASSISTANT")
    print("   Listening continuously in the background...")
    print("=" * 60)

    # Initialize speech recognition
    import speech_recognition as sr
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    r.pause_threshold = 1.1
    r.non_speaking_duration = 0.8
    
    try:
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1.2)
            if r.energy_threshold < 250:
                r.energy_threshold = 250
    except Exception as e:
        logging.error(f"Microphone initialization failed: {e}")
        voice_engine.speak("Microphone hardware error. Please check your audio settings.")
        return

    # Announce ready status through speakers
    user_name = brain.memory.get_user_name() or "my friend"
    startup_greeting = f"SAMPAN is online and listening closely in the background, {user_name}."
    logging.info(f"Speaking: {startup_greeting}")
    voice_engine.speak(startup_greeting)

    last_cmd_text = ""
    last_cmd_time = 0.0

    while True:
        try:
            with mic as source:
                audio = r.listen(source, timeout=6, phrase_time_limit=15)
            
            raw_text = ""
            # Multi-accent recognition: primary en-IN with fallback to en-US
            try:
                raw_text = r.recognize_google(audio, language="en-IN").strip()
            except (sr.UnknownValueError, sr.RequestError):
                pass

            if not raw_text:
                try:
                    raw_text = r.recognize_google(audio, language="en-US").strip()
                except Exception:
                    raw_text = ""

            now = time.time()
            if not raw_text:
                continue

            # Duplicate suppression within 2.0 seconds
            if raw_text.lower() == last_cmd_text and (now - last_cmd_time) < 2.0:
                continue
            
            last_cmd_text = raw_text.lower()
            last_cmd_time = now

            logging.info(f"Heard user speech: '{raw_text}'")
            print(f"\n[Heard]: \"{raw_text}\"")
            
            # Process with SAMPAN Brain
            res = brain.process_command(raw_text)
            speech = res.get("speech", "")
            action = res.get("action", "")
            logging.info(f"SAMPAN response: '{speech}' (Action: {action})")
            print(f"[SAMPAN]: \"{speech}\"")

            # Speak directly through laptop speakers (blocks while speaking to avoid mic feedback)
            if speech:
                voice_engine.speak(speech)

            # Handle shutdown command
            if action == "shutdown_sampan":
                logging.info("Shutting down background service.")
                time.sleep(1.0)
                os._exit(0)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            logging.warning(f"Listen loop warning: {e}")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
