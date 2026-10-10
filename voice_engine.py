"""
JARVIS Voice Engine - High-Fidelity British Neural Speech Synthesis
Uses edge-tts with the 'en-GB-RyanNeural' (or 'en-GB-ThomasNeural') voice
to match the movie Jarvis, with Windows SAPI / PowerShell offline fallback.
"""

import os
import sys
import asyncio
import tempfile
import subprocess
from pathlib import Path

# Preferred Jarvis voices
JARVIS_VOICE = "en-GB-RyanNeural"     # Sounds very close to Paul Bettany's Jarvis
JARVIS_VOICE_ALT = "en-GB-ThomasNeural"

CACHE_DIR = Path(__file__).parent / "static" / "audio_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

async def _synthesize_edge_tts(text: str, output_path: str, voice: str = JARVIS_VOICE, rate: str = "+0%", pitch: str = "+0Hz"):
    """Synthesizes text using Microsoft Edge Neural TTS."""
    import edge_tts
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return output_path

def synthesize_speech(text: str, voice: str = JARVIS_VOICE, rate: str = "+0%") -> str:
    """
    Synthesizes speech to an MP3 file and returns the relative or absolute filepath.
    Falls back gracefully if edge-tts fails.
    """
    import hashlib
    # Cache key based on text and voice
    text_hash = hashlib.md5(f"{text}_{voice}_{rate}".encode("utf-8")).hexdigest()
    out_file = CACHE_DIR / f"jarvis_{text_hash}.mp3"

    if out_file.exists() and out_file.stat().st_size > 0:
        return str(out_file)

    try:
        try:
            asyncio.run(_synthesize_edge_tts(text, str(out_file), voice, rate))
        except RuntimeError:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pool.submit(lambda: asyncio.run(_synthesize_edge_tts(text, str(out_file), voice, rate))).result(timeout=10)

        if out_file.exists() and out_file.stat().st_size > 0:
            return str(out_file)
    except Exception as e:
        print(f"[JARVIS Voice Warning] edge-tts error: {e}. Falling back to Windows SAPI.", file=sys.stderr)

    # Fallback to Windows SAPI via PowerShell (offline, guaranteed on Windows)
    wav_file = CACHE_DIR / f"jarvis_{text_hash}.wav"
    try:
        escaped_text = text.replace('"', '`"').replace("'", "''")
        ps_cmd = (
            f'Add-Type -AssemblyName System.Speech; '
            f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            f'$synth.SetOutputToWaveFile("{wav_file}"); '
            f'$synth.Speak("{escaped_text}"); '
            f'$synth.Dispose()'
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True, timeout=10)
        if wav_file.exists():
            return str(wav_file)
    except Exception as ps_err:
        print(f"[JARVIS Voice Error] Fallback synthesis failed: {ps_err}", file=sys.stderr)

    return ""

def speak_direct(text: str):
    """Speaks directly on the system speakers (for background/terminal alerts)."""
    try:
        escaped_text = text.replace('"', '`"').replace("'", "''")
        ps_cmd = (
            f'Add-Type -AssemblyName System.Speech; '
            f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            f'$synth.Speak("{escaped_text}")'
        )
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_cmd])
    except Exception as e:
        print(f"[JARVIS Speech] Direct speak failed: {e}")

if __name__ == "__main__":
    test_phrase = "Good evening, sir. All core systems are online and fully operational."
    print("Testing synthesis for:", test_phrase)
    f = synthesize_speech(test_phrase)
    print("Synthesized audio file:", f)
