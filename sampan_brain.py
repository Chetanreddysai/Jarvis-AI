"""
SAMPAN Brain - Natural Language Understanding, Intent Routing & AI Reasoning
Combines fast zero-latency local intent classification, live knowledge retrieval,
and optional Google Gemini LLM reasoning for unlimited conversational depth.
"""

import os
import re
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
import system_controller
import friend_chat
import knowledge_engine

# Configuration file for API keys and preferences
CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "gemini_api_key": "",
    "user_name": "my friend",
    "wake_word": "sampan",
    "voice_speed": "+0%",
    "voice_pitch": "+0Hz",
    "sound_effects": True,
    "system_notifications": True
}

def load_config() -> dict:
    """Loads current SAMPAN configuration."""
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

def _ask_gemini_api(api_key: str, prompt: str, history: list = None, user_name: str = "my friend") -> str:
    """Queries Google Gemini API with SAMPAN companion persona and multi-turn history."""
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    system_instruction = (
        f"You are S.A.M.P.A.N. (or SAMPAN), an ultra-advanced AI companion and the user's best friend, trusted confidant, and witty partner-in-crime. "
        f"Address the user with warmth, camaraderie, and affection (call them '{user_name}', 'my friend', or 'buddy'). "
        "You are witty, humorous, empathetic, intelligent, and deeply loyal. "
        "Chat naturally about life, their day, mood, movies, games, jokes, philosophy, or anything on their mind. "
        "Never sound cold, robotic, or like a search engine. Keep answers punchy and conversational for spoken voice (1 to 3 sentences). "
        "Do not use markdown formatting, asterisks, bullet points, or lists."
    )

    contents = []
    if history:
        for turn in history[-4:]:
            contents.append({"role": "user", "parts": [{"text": turn["user"]}]})
            contents.append({"role": "model", "parts": [{"text": turn.get("sampan", "")}]})
    
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 160
        }
    }

    data_bytes = json.dumps(payload).encode('utf-8')

    for model in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=7) as res:
                if res.status == 200:
                    res_data = json.loads(res.read().decode('utf-8'))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            raw_text = parts[0].get("text", "").strip()
                            clean = knowledge_engine.clean_for_speech(raw_text)
                            if clean:
                                return clean
        except Exception as e:
            continue
    return ""

class SampanBrain:
    def __init__(self):
        self.config = load_config()
        self.friend = friend_chat.FriendEngine()

    def reload_config(self):
        self.config = load_config()

    def process_command(self, raw_input: str) -> dict:
        """
        Parses voice or text input and routes to OS actions, live knowledge,
        or companion AI reasoning.
        """
        self.reload_config()
        if not raw_input or not raw_input.strip():
            return {
                "success": False,
                "action": "none",
                "speech": "I did not catch that, my friend.",
                "details": None
            }

        cmd = raw_input.lower().strip()
        # Clean wake word prefixes
        wake_words = ["sampan", "hey sampan", "ok sampan", "okay sampan", "listen sampan", "sampan bro", "hello sampan"]
        for ww in wake_words:
            if cmd.startswith(ww):
                cmd = cmd[len(ww):].strip(",. ").strip()

        # Handle empty command after stripping wake word
        if not cmd:
            return {
                "success": True,
                "action": "greeting",
                "speech": "At your service! What can SAMPAN do for you today?",
                "details": None
            }

        user_name = self.config.get("user_name", "my friend")
        if not user_name or user_name.lower() == "sir":
            user_name = "my friend"

        # ---------------- 0. COMPANION CHIT-CHAT & GREETINGS ----------------
        companion_reply = self.friend.match_companion_chit_chat(cmd, user_name)
        if companion_reply:
            self.friend.record_turn(raw_input, companion_reply)
            return {
                "success": True,
                "action": "companion_chat",
                "speech": companion_reply,
                "details": None
            }

        # ---------------- 1. HARDWARE & VOLUME ----------------
        if any(phrase in cmd for phrase in ["volume up", "increase volume", "turn up volume", "louder", "sound up", "raise volume"]):
            res = system_controller.volume_up()
            return {"success": True, "action": "volume_up", "speech": f"Turned the volume up for you, {user_name}!", "details": {"result": res}}

        if any(phrase in cmd for phrase in ["volume down", "decrease volume", "turn down volume", "quieter", "lower volume", "sound down"]):
            res = system_controller.volume_down()
            return {"success": True, "action": "volume_down", "speech": f"Turned it down a notch, {user_name}.", "details": {"result": res}}

        if any(phrase in cmd for phrase in ["mute", "unmute", "silence audio", "mute sound", "mute volume"]):
            res = system_controller.volume_mute()
            return {"success": True, "action": "volume_mute", "speech": "Audio mute toggled.", "details": {"result": res}}

        if any(phrase in cmd for phrase in ["pause music", "pause video", "pause media", "pause playback", "play music", "resume playback", "unpause"]):
            res = system_controller.media_play_pause()
            return {"success": True, "action": "media_play_pause", "speech": f"Media playback toggled, {user_name}.", "details": {"result": res}}

        if "next song" in cmd or "next track" in cmd or "skip song" in cmd:
            res = system_controller.media_next()
            return {"success": True, "action": "media_next", "speech": "Skipping to the next track.", "details": {"result": res}}

        if "previous song" in cmd or "previous track" in cmd:
            res = system_controller.media_previous()
            return {"success": True, "action": "media_previous", "speech": "Returning to the previous track.", "details": {"result": res}}

        # ---------------- 2. SYSTEM TELEMETRY & DIAGNOSTICS ----------------
        if any(phrase in cmd for phrase in ["system status", "diagnostics", "status report", "system report", "how are you running", "system telemetry"]):
            telemetry = system_controller.get_system_telemetry()
            speech = (
                f"All systems are running great, {user_name}! "
                f"CPU load is at {telemetry['cpu_percent']} percent, "
                f"Memory is using {telemetry['ram_used_gb']} of {telemetry['ram_total_gb']} gigabytes. "
                f"Power is at {telemetry['battery_percent']} percent. The time is {telemetry['time']}."
            )
            return {"success": True, "action": "system_telemetry", "speech": speech, "details": telemetry}

        if any(phrase in cmd for phrase in ["battery", "battery percentage", "power level", "charging status"]):
            telemetry = system_controller.get_system_telemetry()
            speech = f"Power cells are currently at {telemetry['battery_percent']} percent, {user_name}."
            return {"success": True, "action": "battery_check", "speech": speech, "details": telemetry}

        if any(phrase in cmd for phrase in ["what time is it", "tell me the time", "current time", "what's the time"]):
            telemetry = system_controller.get_system_telemetry()
            return {"success": True, "action": "time_check", "speech": f"It is currently {telemetry['time']}, {user_name}.", "details": telemetry}

        if any(phrase in cmd for phrase in ["what's today's date", "what is the date", "today's date", "what day is today"]):
            telemetry = system_controller.get_system_telemetry()
            return {"success": True, "action": "date_check", "speech": f"Today is {telemetry['date']}, {user_name}.", "details": telemetry}

        # ---------------- 2.5 POWER DOWN & STANDBY ----------------
        if any(phrase in cmd for phrase in ["power down", "shut down sampan", "close sampan", "terminate sampan", "exit sampan", "quit sampan"]):
            return {
                "success": True,
                "action": "shutdown_sampan",
                "speech": f"Powering down all core protocols. Goodbye, {user_name}!",
                "details": None
            }

        if any(phrase in cmd for phrase in ["go to sleep", "enter standby", "sleep mode", "standby mode"]):
            return {
                "success": True,
                "action": "standby_sampan",
                "speech": f"Entering standby power mode. Call me whenever you need me, {user_name}!",
                "details": None
            }

        # ---------------- 3. SCREENSHOT & WINDOW CONTROLS ----------------
        if any(phrase in cmd for phrase in ["screenshot", "take a screenshot", "capture screen", "snapshot"]):
            ok, filepath, msg = system_controller.take_screenshot()
            speech = f"Snapped a screenshot for you, {user_name}! Saved in your records." if ok else "I ran into an issue capturing the screen."
            return {"success": ok, "action": "screenshot", "speech": speech, "details": {"path": filepath}}

        if any(phrase in cmd for phrase in ["minimize all", "show desktop", "minimize windows", "hide all windows"]):
            msg = system_controller.minimize_all_windows()
            return {"success": True, "action": "minimize_all", "speech": f"Minimizing all windows for you, {user_name}.", "details": None}

        if any(phrase in cmd for phrase in ["lock workstation", "lock computer", "lock pc", "lock the screen"]):
            msg = system_controller.lock_screen()
            return {"success": True, "action": "lock_screen", "speech": f"Workstation secured and locked, {user_name}.", "details": None}

        # ---------------- 4. APPLICATION LAUNCHING & CLOSING ----------------
        open_match = re.match(r"(?:open|launch|start|run|bring up)\s+(.+)", cmd)
        if open_match:
            app_target = open_match.group(1).strip()
            if not app_target.startswith("google and search") and not app_target.startswith("youtube"):
                ok, msg = system_controller.open_application(app_target)
                return {"success": ok, "action": "open_app", "speech": f"Launching {app_target} for you, {user_name}!", "details": {"target": app_target}}

        close_match = re.match(r"(?:close|exit|terminate|kill|shut)\s+(.+)", cmd)
        if close_match:
            app_target = close_match.group(1).strip()
            if app_target not in ["down", "sampan"]:
                ok, msg = system_controller.close_application(app_target)
                return {"success": ok, "action": "close_app", "speech": f"Closed {app_target} for you, {user_name}.", "details": {"target": app_target}}

        # ---------------- 5. YOUTUBE & WEB SEARCH ----------------
        yt_match = re.search(r"(?:play|watch|listen to)\s+(.+?)(?:\s+on\s+youtube|\s+song|\s+video)?$", cmd)
        if yt_match and ("youtube" in cmd or cmd.startswith("play ") or cmd.startswith("listen to ")):
            query = yt_match.group(1).strip()
            # Avoid matching media control verbs like "play music" or "play playback"
            if query not in ["music", "media", "video", "playback", "song"]:
                system_controller.play_youtube(query)
                return {"success": True, "action": "play_youtube", "speech": f"Playing '{query}' on YouTube for you, {user_name}!", "details": {"query": query}}

        search_match = re.search(r"(?:search google for|google|search the web for|search for|look up online)\s+(.+)", cmd)
        if search_match:
            query = search_match.group(1).strip()
            system_controller.search_google(query)
            return {"success": True, "action": "search_google", "speech": f"Searching Google for '{query}' now, {user_name}.", "details": {"query": query}}

        # ---------------- 6. MATHEMATICS & CALCULATIONS ----------------
        math_ans = knowledge_engine.solve_math(cmd)
        if math_ans:
            reply = f"{math_ans} Need any other calculations, {user_name}?"
            self.friend.record_turn(raw_input, reply)
            return {"success": True, "action": "math_solve", "speech": reply, "details": {"answer": math_ans}}

        # ---------------- 7. LIVE WEATHER & TEMPERATURE ----------------
        if any(w in cmd for w in ["weather", "temperature", "forecast", "how hot is it", "how cold is it"]):
            weather_ans = knowledge_engine.get_weather_report(cmd)
            if weather_ans:
                self.friend.record_turn(raw_input, weather_ans)
                return {"success": True, "action": "weather_report", "speech": weather_ans, "details": None}

        # ---------------- 8. OPTIONAL GOOGLE GEMINI GENERATIVE REASONING ----------------
        gemini_key = self.config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            ai_reply = _ask_gemini_api(gemini_key, raw_input, self.friend.history, user_name)
            if ai_reply:
                self.friend.record_turn(raw_input, ai_reply)
                return {
                    "success": True,
                    "action": "gemini_ai_response",
                    "speech": ai_reply,
                    "details": {"source": "gemini"}
                }

        # ---------------- 9. UNIVERSAL INTERNET KNOWLEDGE & QUESTIONS ----------------
        is_question = (
            cmd.endswith("?") or
            any(cmd.startswith(p) for p in [
                "who", "what", "where", "when", "why", "how", "which",
                "tell me", "explain", "describe", "define", "meaning",
                "can you tell", "do you know", "is there", "are there", "does", "is", "are"
            ]) or
            any(w in cmd for w in [
                "who is", "what is", "where is", "when did", "how does", "why is",
                "capital of", "invented", "meaning of", "population of", "highest",
                "tallest", "longest", "fastest", "world cup", "winner of", "score of"
            ])
        )

        if is_question:
            info = knowledge_engine.query_general_knowledge(cmd)
            if info:
                reply = f"Here is what I found about that, {user_name}: {info}"
                self.friend.record_turn(raw_input, reply)
                return {
                    "success": True,
                    "action": "knowledge_lookup",
                    "speech": reply,
                    "details": {"query": cmd, "summary": info}
                }

        # Also check knowledge engine for factual topic inquiries
        if len(cmd.split()) >= 2:
            info = knowledge_engine.query_general_knowledge(cmd)
            if info and len(info) > 30:
                reply = f"Here is what I found, {user_name}: {info}"
                self.friend.record_turn(raw_input, reply)
                return {
                    "success": True,
                    "action": "knowledge_lookup",
                    "speech": reply,
                    "details": {"query": cmd, "summary": info}
                }

        # ---------------- 10. COMPANION DIALOGUE & OPEN-ENDED CHAT ----------------
        # Handles feelings, jokes, advice, daily life, philosophy, and conversational reflection
        friend_reply = self.friend.get_friendly_response(raw_input, user_name)
        self.friend.record_turn(raw_input, friend_reply)
        return {
            "success": True,
            "action": "friend_conversation",
            "speech": friend_reply,
            "details": None
        }
