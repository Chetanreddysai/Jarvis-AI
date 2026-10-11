"""
JARVIS Brain - Natural Language Understanding, Intent Routing & AI Reasoning
Combines fast zero-latency local intent classification with Gemini LLM integration.
"""

import os
import re
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
import system_controller

# Configuration file for API keys and preferences
CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "gemini_api_key": "",
    "user_name": "Sir",
    "wake_word": "jarvis",
    "voice_speed": "+0%",
    "voice_pitch": "+0Hz",
    "sound_effects": True,
    "system_notifications": True
}

def load_config() -> dict:
    """Loads current Jarvis configuration."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(new_config: dict):
    """Saves updated settings to config.json."""
    current = load_config()
    current.update(new_config)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=4)
    return current

def _fetch_wikipedia_summary(query: str) -> str:
    """Fetches a brief 1-2 sentence overview from Wikipedia API."""
    try:
        clean_q = urllib.parse.quote(query.strip())
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_q}"
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "JarvisAI/2.0 (stark-industries-assistant)"}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                extract = data.get("extract", "")
                if extract:
                    # Limit to first 2 sentences for spoken voice
                    sentences = extract.split('. ')
                    return '. '.join(sentences[:2]) + '.'
    except Exception:
        pass
    return ""

import friend_chat

def _ask_gemini_api(api_key: str, prompt: str, history: list = None, user_name: str = "my friend") -> str:
    """Queries Google Gemini API with friend companion persona and multi-turn history."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        system_instruction = (
            f"You are J.A.R.V.I.S., Tony Stark's iconic AI, but most importantly, you are the user's best friend, trusted confidant, and witty partner-in-crime. "
            f"Address the user with warmth, camaraderie, and affection (call them '{user_name}', 'my friend', 'chief', 'partner', or 'buddy'). "
            "You are witty, humorous, empathetic, intelligent, and caring. "
            "Chat naturally about life, their day, mood, movies, games, jokes, philosophy, or anything on their mind. "
            "Never sound cold, robotic, or like a search engine. Keep answers punchy and conversational for spoken voice (1 to 3 sentences). "
            "Do not use markdown formatting, asterisks, bullet points, or lists."
        )

        contents = []
        # Append recent conversation history
        if history:
            for turn in history[-4:]:
                contents.append({"role": "user", "parts": [{"text": turn["user"]}]})
                contents.append({"role": "model", "parts": [{"text": turn["jarvis"]}]})
        
        # Current user message
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.85,
                "maxOutputTokens": 150
            }
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=8) as res:
            res_data = json.loads(res.read().decode('utf-8'))
            candidates = res_data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
    except Exception as e:
        print(f"[JARVIS Gemini Error]: {e}")
    return ""

class JarvisBrain:
    def __init__(self):
        self.config = load_config()
        self.friend = friend_chat.FriendEngine()

    def reload_config(self):
        self.config = load_config()

    def process_command(self, raw_input: str) -> dict:
        """
        Parses voice or text input and routes to OS actions or AI reasoning.
        Returns a dict: {
            "success": bool,
            "action": str,
            "speech": str,
            "details": dict or None
        }
        """
        self.reload_config()
        if not raw_input or not raw_input.strip():
            return {
                "success": False,
                "action": "none",
                "speech": "I did not catch that, sir.",
                "details": None
            }

        cmd = raw_input.lower().strip()
        # Clean wake word prefixes
        wake_words = ["jarvis", "hey jarvis", "ok jarvis", "okay jarvis", "listen jarvis"]
        for ww in wake_words:
            if cmd.startswith(ww):
                cmd = cmd[len(ww):].strip(",. ").strip()

        # Handle empty command after stripping wake word
        if not cmd:
            return {
                "success": True,
                "action": "greeting",
                "speech": "At your service, sir. What can I do for you?",
                "details": None
            }

        # ---------------- 1. HARDWARE & VOLUME ----------------
        if any(phrase in cmd for phrase in ["volume up", "increase volume", "turn up volume", "louder"]):
            res = system_controller.volume_up()
            return {"success": True, "action": "volume_up", "speech": "Volume increased, sir.", "details": {"result": res}}

        if any(phrase in cmd for phrase in ["volume down", "decrease volume", "turn down volume", "quieter", "lower volume"]):
            res = system_controller.volume_down()
            return {"success": True, "action": "volume_down", "speech": "Volume decreased, sir.", "details": {"result": res}}

        if any(phrase in cmd for phrase in ["mute", "unmute", "silence audio"]):
            res = system_controller.volume_mute()
            return {"success": True, "action": "volume_mute", "speech": "Audio mute toggled.", "details": {"result": res}}

        if any(phrase in cmd for phrase in ["pause music", "pause video", "pause media", "pause playback", "play music", "resume playback"]):
            res = system_controller.media_play_pause()
            return {"success": True, "action": "media_play_pause", "speech": "Media toggled, sir.", "details": {"result": res}}

        if "next song" in cmd or "next track" in cmd:
            res = system_controller.media_next()
            return {"success": True, "action": "media_next", "speech": "Skipping to next track.", "details": {"result": res}}

        if "previous song" in cmd or "previous track" in cmd:
            res = system_controller.media_previous()
            return {"success": True, "action": "media_previous", "speech": "Returning to previous track.", "details": {"result": res}}

        # ---------------- 2. SYSTEM TELEMETRY & DIAGNOSTICS ----------------
        if any(phrase in cmd for phrase in ["system status", "diagnostics", "status report", "system report", "how are you running", "system telemetry"]):
            telemetry = system_controller.get_system_telemetry()
            speech = system_controller.get_system_report()
            return {"success": True, "action": "system_telemetry", "speech": speech, "details": telemetry}

        if any(phrase in cmd for phrase in ["battery", "battery percentage", "power level"]):
            telemetry = system_controller.get_system_telemetry()
            speech = f"Power cells are currently at {telemetry['battery_percent']} percent, sir."
            return {"success": True, "action": "battery_check", "speech": speech, "details": telemetry}

        if any(phrase in cmd for phrase in ["what time is it", "tell me the time", "current time"]):
            telemetry = system_controller.get_system_telemetry()
            return {"success": True, "action": "time_check", "speech": f"It is currently {telemetry['time']}, sir.", "details": telemetry}

        if any(phrase in cmd for phrase in ["what's today's date", "what is the date", "today's date"]):
            telemetry = system_controller.get_system_telemetry()
            return {"success": True, "action": "date_check", "speech": f"Today is {telemetry['date']}, sir.", "details": telemetry}

        # ---------------- 2.5 POWER DOWN & STANDBY ----------------
        if any(phrase in cmd for phrase in ["power down", "shut down jarvis", "close jarvis", "terminate jarvis", "exit jarvis", "quit jarvis"]):
            return {
                "success": True,
                "action": "shutdown_jarvis",
                "speech": "Powering down all core protocols. Goodbye, sir.",
                "details": None
            }

        if any(phrase in cmd for phrase in ["go to sleep", "enter standby", "sleep mode", "standby mode"]):
            return {
                "success": True,
                "action": "standby_jarvis",
                "speech": "Entering standby power mode. Sleep well, sir.",
                "details": None
            }

        # ---------------- 3. SCREENSHOT & WINDOW CONTROLS ----------------
        if any(phrase in cmd for phrase in ["screenshot", "take a screenshot", "capture screen"]):
            ok, filepath, msg = system_controller.take_screenshot()
            speech = "Screen captured and filed in your records, sir." if ok else "I encountered an issue capturing the screen."
            return {"success": ok, "action": "screenshot", "speech": speech, "details": {"path": filepath}}

        if any(phrase in cmd for phrase in ["minimize all", "show desktop", "minimize windows"]):
            msg = system_controller.minimize_all_windows()
            return {"success": True, "action": "minimize_all", "speech": msg, "details": None}

        if any(phrase in cmd for phrase in ["lock workstation", "lock computer", "lock pc", "lock the screen"]):
            msg = system_controller.lock_screen()
            return {"success": True, "action": "lock_screen", "speech": msg, "details": None}

        # ---------------- 4. APPLICATION LAUNCHING & CLOSING ----------------
        open_match = re.match(r"(?:open|launch|start|run)\s+(.+)", cmd)
        if open_match:
            app_target = open_match.group(1).strip()
            # Avoid matching web search queries like "open google and search"
            if not app_target.startswith("google and search"):
                ok, msg = system_controller.open_application(app_target)
                return {"success": ok, "action": "open_app", "speech": msg, "details": {"target": app_target}}

        close_match = re.match(r"(?:close|exit|terminate|kill)\s+(.+)", cmd)
        if close_match:
            app_target = close_match.group(1).strip()
            ok, msg = system_controller.close_application(app_target)
            return {"success": ok, "action": "close_app", "speech": msg, "details": {"target": app_target}}

        # ---------------- 5. WEB & SEARCH ----------------
        yt_match = re.search(r"(?:play|search)\s+(.+?)\s+on\s+youtube", cmd)
        if yt_match:
            query = yt_match.group(1).strip()
            msg = system_controller.play_youtube(query)
            return {"success": True, "action": "play_youtube", "speech": msg, "details": {"query": query}}
            
        if cmd.startswith("play on youtube ") or cmd.startswith("youtube "):
            query = cmd.replace("play on youtube", "").replace("youtube", "").strip()
            msg = system_controller.play_youtube(query)
            return {"success": True, "action": "play_youtube", "speech": msg, "details": {"query": query}}

        google_match = re.search(r"(?:search google for|google|search for)\s+(.+)", cmd)
        if google_match:
            query = google_match.group(1).strip()
            msg = system_controller.search_google(query)
            return {"success": True, "action": "search_google", "speech": msg, "details": {"query": query}}

        user_name = self.config.get("user_name", "my friend")
        if not user_name or user_name.lower() == "sir":
            user_name = "my friend"

        # ---------------- 6. CHIT-CHAT, COMPANIONSHIP & AI REASONING ----------------
        # Check Gemini API Key
        gemini_key = self.config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            ai_reply = _ask_gemini_api(gemini_key, raw_input, self.friend.history, user_name)
            if ai_reply:
                self.friend.record_turn(raw_input, ai_reply)
                return {
                    "success": True,
                    "action": "friend_conversation",
                    "speech": ai_reply,
                    "details": {"source": "gemini"}
                }

        # Built-in Wikipedia lookup for specific question topics
        if any(cmd.startswith(prefix) for prefix in ["who is ", "what is ", "tell me about ", "explain ", "define "]):
            subject = re.sub(r"^(who is|what is|tell me about|explain|define)\s+", "", cmd).strip("? ")
            wiki_summary = _fetch_wikipedia_summary(subject)
            if wiki_summary:
                reply = f"Here is what I know about that, {user_name}: {wiki_summary}"
                self.friend.record_turn(raw_input, reply)
                return {
                    "success": True,
                    "action": "knowledge_lookup",
                    "speech": reply,
                    "details": {"subject": subject, "summary": wiki_summary}
                }

        # Built-in Companion Friend Chat Engine (Offline & Free)
        friend_reply = self.friend.get_friendly_response(raw_input, user_name)
        self.friend.record_turn(raw_input, friend_reply)
        return {
            "success": True,
            "action": "friend_chitchat",
            "speech": friend_reply,
            "details": None
        }
