"""
SAMPAN Memory & Learning Engine
Persistently stores user identity, preferences, notes, reminders,
and custom learned command shortcuts in a local JSON database.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "sampan_memory.json"

DEFAULT_MEMORY = {
    "user_profile": {
        "name": "",
        "likes": [],
        "facts": []
    },
    "notes": [],
    "learned_shortcuts": {},
    "recent_topics": []
}

class MemoryEngine:
    def __init__(self):
        self.memory_path = MEMORY_FILE
        self.data = self._load()

    def _load(self) -> dict:
        if self.memory_path.exists():
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    return {**DEFAULT_MEMORY, **loaded}
            except Exception:
                pass
        return DEFAULT_MEMORY.copy()

    def save(self):
        try:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"[Memory Save Error]: {e}")

    # ================= USER PROFILE & NAME =================

    def set_user_name(self, name: str) -> str:
        clean = name.strip().title()
        self.data["user_profile"]["name"] = clean
        self.save()
        return clean

    def get_user_name(self) -> str:
        return self.data["user_profile"].get("name", "").strip()

    def add_user_fact(self, fact: str) -> str:
        clean_fact = fact.strip()
        if clean_fact and clean_fact not in self.data["user_profile"]["facts"]:
            self.data["user_profile"]["facts"].append(clean_fact)
            self.save()
            return f"I've memorized that: {clean_fact}"
        return "I already remember that, my friend!"

    def get_all_facts(self) -> list:
        return self.data["user_profile"].get("facts", [])

    # ================= NOTES & REMINDERS =================

    def add_note(self, text: str) -> str:
        clean = text.strip()
        if not clean:
            return ""
        now_str = datetime.now().strftime("%I:%M %p, %d %b")
        note_entry = {
            "id": len(self.data["notes"]) + 1,
            "text": clean,
            "created_at": now_str
        }
        self.data["notes"].append(note_entry)
        self.save()
        return f"Noted down: '{clean}'"

    def get_notes(self) -> list:
        return [n["text"] for n in self.data.get("notes", [])]

    def clear_notes(self) -> str:
        count = len(self.data.get("notes", []))
        self.data["notes"] = []
        self.save()
        return f"Cleared {count} notes from your memory records."

    # ================= CUSTOM SHORTCUTS / SKILL LEARNING =================

    def learn_shortcut(self, trigger: str, action: str) -> str:
        clean_trig = trigger.lower().strip()
        clean_act = action.strip()
        if clean_trig and clean_act:
            self.data["learned_shortcuts"][clean_trig] = clean_act
            self.save()
            return f"I've learned a new skill! Whenever you say '{clean_trig}', I will execute '{clean_act}'."
        return "Could not understand that command shortcut format."

    def get_shortcut(self, phrase: str) -> str | None:
        clean = phrase.lower().strip()
        return self.data.get("learned_shortcuts", {}).get(clean)

    # ================= CONVERSATION TOPIC MEMORY =================

    def record_topic(self, topic: str):
        if not topic:
            return
        topics = self.data.get("recent_topics", [])
        topics.append(topic)
        if len(topics) > 10:
            topics.pop(0)
        self.data["recent_topics"] = topics
        self.save()

    def get_recent_topics(self) -> list:
        return self.data.get("recent_topics", [])

    # ================= NATURAL LANGUAGE MEMORY RECALL =================

    def handle_memory_request(self, command: str, default_name: str = "my friend") -> str | None:
        clean = command.lower().strip()

        # 1. Learning Name: "my name is Chetan", "call me Chetan", "remember my name is Chetan"
        name_match = re.search(r'(?:my name is|call me|remember my name is)\s+([a-zA-Z]+)', clean)
        if name_match:
            new_name = name_match.group(1).strip()
            self.set_user_name(new_name)
            return f"Pleasure to officially remember you, {new_name}! I've stored your name permanently in my core memory."

        # 2. Who am I / What is my name:
        if any(p in clean for p in ["what is my name", "who am i", "do you know my name", "what's my name"]):
            saved = self.get_user_name()
            if saved:
                return f"You are {saved}, my trusted friend and partner!"
            return "You haven't told me your name yet! Just say 'My name is [your name]' and I will remember."

        # 3. Learning Facts: "remember that I like ...", "remember that my ...", "keep in mind that ..."
        fact_match = re.search(r'(?:remember that|keep in mind that|note that)\s+(.+)', clean)
        if fact_match:
            fact_content = fact_match.group(1).strip()
            # If it's a note/reminder
            if any(w in fact_content for w in ["have to", "need to", "meeting", "exam", "buy", "call", "appointment"]):
                self.add_note(fact_content)
                return f"Got it, {default_name}! I have saved that reminder in your notes: '{fact_content}'."
            else:
                self.add_user_fact(fact_content)
                return f"Understood, {default_name}! I'll permanently remember that: {fact_content}."

        # 4. Learning Custom Shortcuts: "when I say [X], [action]" or "teach you: [X] means [action]"
        shortcut_match = re.search(r'(?:when i say|whenever i say)\s+["\']?([^,\'"]+?)["\']?\s*(?:,\s*|\s+then\s+|\s+please\s+|\s+meaning\s+)(.+)', clean)
        if not shortcut_match:
            shortcut_match = re.search(r'(?:teach you\s*:?\s*)["\']?([^,\'"]+?)["\']?\s*(?:means|is)\s+(.+)', clean)
        if shortcut_match:
            trig = shortcut_match.group(1).strip()
            act = shortcut_match.group(2).strip()
            return self.learn_shortcut(trig, act)

        # 5. Asking what is remembered: "what do you remember about me", "what are my notes", "show my notes"
        if any(p in clean for p in ["what do you remember", "what do you know about me", "my profile", "what have you learned"]):
            name = self.get_user_name() or default_name
            facts = self.get_all_facts()
            notes = self.get_notes()
            shortcuts = list(self.data.get("learned_shortcuts", {}).keys())

            parts = [f"Here is what I have learned about you, {name}:"]
            if facts:
                parts.append("Facts: " + "; ".join(facts[:3]) + ".")
            if notes:
                parts.append("Recent notes: " + "; ".join(notes[:3]) + ".")
            if shortcuts:
                parts.append("Custom shortcuts: " + ", ".join(shortcuts) + ".")
            if len(parts) == 1:
                parts.append("I haven't stored many custom details yet. Tell me 'remember that [something]' to teach me!")
            return " ".join(parts)

        if any(p in clean for p in ["what are my notes", "show my notes", "read my notes", "list my notes"]):
            notes = self.get_notes()
            if notes:
                return f"You have {len(notes)} saved notes, {default_name}: " + ". ".join(notes) + "."
            return f"You don't have any saved notes right now, {default_name}."

        if any(p in clean for p in ["clear my notes", "delete my notes", "erase notes"]):
            return self.clear_notes()

        # 6. Recalling recent conversation: "what did we just talk about", "what were we talking about"
        if any(p in clean for p in ["what did we just talk about", "what were we talking about", "what did i just say"]):
            topics = self.get_recent_topics()
            if topics:
                last_few = ", ".join(topics[-3:])
                return f"Recently we were talking about: {last_few}."
            return "We just started our conversation, my friend!"

        return None
