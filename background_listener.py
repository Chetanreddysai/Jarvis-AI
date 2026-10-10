"""
JARVIS Headless Background Voice Listener (Optional Mode)
Listens continuously via system microphone using SpeechRecognition,
executing commands and speaking responses even when no window is visible.
"""

import sys
import time
import speech_recognition as sr
import jarvis_brain
import voice_engine

def run_headless_listener():
    brain = jarvis_brain.JarvisBrain()
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"[JARVIS Error] Microphone initialization failed: {e}")
        print("Note: In Windows, the Web HUD interface provides built-in browser speech recognition without needing PyAudio!")
        return

    print("=" * 60)
    print("   J.A.R.V.I.S. HEADLESS VOICE LISTENER ONLINE")
    print("   Say 'Jarvis [command]' to control your computer.")
    print("=" * 60)

    # Startup greeting
    voice_engine.speak_direct("Good evening, sir. Jarvis background listener is active.")

    with mic as source:
        print("\nAdjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("Listening actively...\n")

        while True:
            try:
                print(">>> Listening...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)
                print(">>> Processing speech...")
                text = recognizer.recognize_google(audio).lower()
                print(f"[You]: {text}")

                if "jarvis" in text or any(text.startswith(w) for w in ["open", "volume", "play", "screenshot", "status"]):
                    result = brain.process_command(text)
                    speech = result.get("speech", "")
                    print(f"[JARVIS]: {speech}")
                    voice_engine.speak_direct(speech)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"[JARVIS Loop Notice]: {e}")
                time.sleep(0.5)

if __name__ == "__main__":
    run_headless_listener()
