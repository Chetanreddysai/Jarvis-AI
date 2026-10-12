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

    # Initialize optimized high-speed speech recognition
    import speech_recognition as sr
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.65       # Fast silence cutoff (reduced from 1.1s)
    r.non_speaking_duration = 0.3  # Snappy audio buffer (reduced from 0.8s)
    
    try:
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.8)
            # Lock firm noise floor so background room noise never delays speech cutoff
            r.energy_threshold = max(300, r.energy_threshold)
            r.dynamic_energy_threshold = False
    except Exception as e:
        logging.error(f"Microphone initialization failed: {e}")
        voice_engine.speak_fast("Microphone hardware error. Please check your audio settings.")
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
            
            # Fast direct speech recognition in user accent
            lang = brain.config.get("speech_language", "en-IN")
            raw_text = ""
            try:
                raw_text = r.recognize_google(audio, language=lang).strip()
            except (sr.UnknownValueError, sr.RequestError):
                pass

            now = time.time()
            if not raw_text:
                continue

            # Duplicate suppression within 1.8 seconds
            if raw_text.lower() == last_cmd_text and (now - last_cmd_time) < 1.8:
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

            # Dual-tier speech: instant SAPI / cached playback for fast actions
            if speech:
                v_mode = brain.config.get("voice_mode", "neural")
                # For rapid hardware actions, prefer fast mode if configured
                voice_engine.speak(speech, mode=v_mode)

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
            time.sleep(0.3)

if __name__ == "__main__":
    main()
