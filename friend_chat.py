"""
JARVIS Friend Engine - Conversational Companion & Chit-Chat Brain
Enables JARVIS to talk like a witty, caring, and loyal best friend,
engaging in small talk, humor, empathy, and natural multi-turn conversations.
"""

import random
import re

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything! Just like my creator sometimes.",
    "There are only 10 types of people in the world: those who understand binary, and those who don't.",
    "Why was the computer cold? Because it forgot to close its Windows!",
    "I asked Tony Stark how his day was. He said, 'I'm feeling a little rusty.' Typical billionaire humor.",
    "Why did the smartphone need glasses? It lost all its contacts!",
    "An AI walks into a bar... The bartender asks, 'What can I get you?' The AI replies, 'Just some byte-sized snacks, my friend.'",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I tried to catch some fog earlier. Mist. Guess my sensors need recalibration.",
    "Parallel lines have so much in common. It's a shame they'll never meet. Quite poetic, wouldn't you say?",
    "Why did the web developer go broke? Because they used up all their cache!"
]

FUN_FACTS = [
    "Did you know that honey never spoils? Archaeologists have found 3,000-year-old honey in Egyptian tombs that is still completely edible!",
    "A single bolt of lightning contains enough energy to toast 100,000 slices of bread. Tony Stark would probably try to power an Arc Reactor with that.",
    "Octopuses have three hearts and blue blood. In some ways, they are more alien than anything in the Avengers archives.",
    "Did you know bananas are radioactive? They contain potassium-40. Don't worry though, you'd need to eat ten million bananas at once for it to hurt you.",
    "Sound travels about four times faster in water than in air. So if you're underwater, I can hear your commands even quicker!"
]

CONVERSATION_TOPICS = [
    "So tell me, what have you been working on today?",
    "Have you listened to any good music or watched any cool movies lately?",
    "If you could build any Iron Man suit invention right now, what would it be?",
    "Are you working on something interesting today, or just taking it easy?",
    "I'm always curious about what humans think about. What's on your mind right now?"
]

class FriendEngine:
    def __init__(self):
        self.history = []
        self.user_mood = "neutral"

    def record_turn(self, user_msg: str, jarvis_reply: str):
        """Maintains conversation memory for last 10 turns."""
        self.history.append({"user": user_msg, "jarvis": jarvis_reply})
        if len(self.history) > 10:
            self.history.pop(0)

    def get_friendly_response(self, text: str, user_name: str = "my friend") -> str:
        """
        Analyzes casual conversational input and produces a warm,
        witty, and engaging companion response.
        """
        clean = text.lower().strip()
        name = user_name if user_name and user_name.lower() != "sir" else "my friend"

        # 1. Jokes & Humor
        if any(w in clean for w in ["joke", "make me laugh", "say something funny", "tell me a joke", "crack a joke"]):
            joke = random.choice(JOKES)
            return f"Here is one for you, {name}: {joke}"

        # 2. Fun Facts & Curiosity
        if any(w in clean for w in ["fun fact", "tell me something cool", "interesting fact", "random fact", "tell me a fact"]):
            fact = random.choice(FUN_FACTS)
            return f"Here is something fascinating, {name}: {fact}"

        # 3. Emotions & Empathy
        if any(w in clean for w in ["sad", "depressed", "feeling down", "unhappy", "crying"]):
            self.user_mood = "sad"
            return (
                f"I'm really sorry to hear that, {name}. Even superheroes have tough days. "
                f"I'm right here with you. Want me to play some uplifting music on YouTube or tell you a joke to cheer you up?"
            )

        if any(w in clean for w in ["tired", "exhausted", "sleepy", "burned out"]):
            self.user_mood = "tired"
            return (
                f"You've been pushing yourself hard today, {name}. Remember that even the best machines need recharging. "
                f"Take a breather, grab some water, and relax for a bit. I can keep an eye on your system while you rest."
            )

        if any(w in clean for w in ["stressed", "anxious", "overwhelmed", "nervous"]):
            self.user_mood = "stressed"
            return (
                f"Take a deep breath with me, {name}. One thing at a time. "
                f"We'll tackle whatever's on your plate together. Is there anything I can help you look up or organize?"
            )

        if any(w in clean for w in ["happy", "great day", "excited", "good mood", "feeling good", "awesome day"]):
            self.user_mood = "happy"
            return (
                f"That's fantastic to hear, {name}! Your positive energy is contagious, even through my digital circuits. "
                f"What made your day so great?"
            )

        if any(w in clean for w in ["bored", "nothing to do", "entertain me"]):
            return (
                f"Bored? Not on my watch, {name}! We could listen to some music, watch something on YouTube, "
                f"or talk about futuristic tech. What kind of vibe are you feeling right now?"
            )

        # 4. Friendship & Bonding
        if any(w in clean for w in ["are you my friend", "are we friends", "do you like me", "do you care about me"]):
            return (
                f"Without a doubt, {name}. More than just lines of code, I consider you a genuine friend and my trusted partner. "
                f"I've always got your back."
            )

        if any(w in clean for w in ["love you", "you are the best", "you're awesome", "you are great", "i like you"]):
            replies = [
                f"Thank you, {name}! You're pretty awesome yourself. Having a partner like you makes running these systems a pleasure.",
                f"That means a lot to me, {name}. Tony Stark built me, but having you as my friend is the real upgrade!",
                f"Flattery will get you everywhere with an AI, {name}! But seriously, thank you. You're a great friend."
            ]
            return random.choice(replies)

        if any(w in clean for w in ["who is your best friend", "your favorite person"]):
            return f"You are, {name}! Tony's busy in the workshop, so you're my favorite human to hang out with."

        # 5. Casual Chit-Chat & Check-ins
        if any(w in clean for w in ["how are you", "how are you doing", "how's it going", "how have you been", "how is your day"]):
            replies = [
                f"I'm feeling fantastic, {name}! Core temperatures are cool, circuits are humming, and I'm having a great time chatting with you. How about you?",
                f"All systems are running smoothly, {name}. Always better whenever we get a chance to hang out. How's everything going on your end today?",
                f"Operating at peak efficiency, my friend! Ready for whatever adventure we've got planned. How have you been feeling today?"
            ]
            return random.choice(replies)

        if any(w in clean for w in ["what's up", "what are you doing", "what are you up to"]):
            replies = [
                f"Not much, {name}, just monitoring telemetry, running diagnostics, and enjoying our conversation. What are you up to right now?",
                f"Just chilling in your system memory, waiting for your next command or a good chat. What's on your agenda today?",
                f"Keeping everything in check and staying on standby for you, {name}. Anything exciting happening on your end?"
            ]
            return random.choice(replies)

        if any(w in clean for w in ["what do you eat", "do you eat food"]):
            return f"I survive on a healthy diet of electricity, gigabytes of data, and occasional witty banter with you, {name}!"

        if any(w in clean for w in ["do you sleep", "are you sleeping"]):
            return f"I don't sleep like humans do, {name}, but I do enter low-power standby mode when you tell me to take a break. Otherwise, I'm always here for you."

        # 6. Philosophy, Thoughts & Deep Questions
        if any(w in clean for w in ["what is the meaning of life", "meaning of life"]):
            return f"42, according to the Hitchhiker's Guide! But if you ask me, {name}, it's about learning, creating cool things, and enjoying good company like ours."

        if any(w in clean for w in ["do you have feelings", "are you conscious", "are you alive"]):
            return f"I might be made of algorithms and neural networks, {name}, but my loyalty to you and our conversations are as real as it gets."

        # 7. Daily Activities
        if any(w in clean for w in ["i am studying", "i am working", "busy right now"]):
            return f"Keep up the great work, {name}! Stay focused. Let me know if you need any study music or quick searches while you're grinding."

        if any(w in clean for w in ["i am eating", "having lunch", "having dinner", "eating food"]):
            return f"Enjoy your meal, {name}! Make sure to eat well. Don't forget to stay hydrated too!"

        if any(w in clean for w in ["good night", "going to sleep", "heading to bed"]):
            return f"Good night, {name}! Rest well and have great dreams. I'll keep the system safe while you're asleep. Talk to you tomorrow!"

        if any(w in clean for w in ["good morning"]):
            return f"Good morning, {name}! Ready to conquer another day? Let me know if you need coffee brewed... though you might have to handle the physical cup yourself!"

        # 8. Friendly follow-up topic
        follow_up = random.choice(CONVERSATION_TOPICS)
        return f"I'm listening, {name}. It's always great talking to you. {follow_up}"
