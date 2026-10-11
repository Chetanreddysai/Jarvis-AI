"""
SAMPAN Friend Engine - Conversational Companion & Multi-Turn Dialogue Brain
Enables SAMPAN to talk like a witty, caring, and loyal best friend,
understanding open-ended conversation, mood, daily life, philosophy, and ideas.
"""

import random
import re

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything! Just like Tony Stark sometimes.",
    "There are only 10 types of people in the world: those who understand binary, and those who don't.",
    "Why was the computer cold? Because it forgot to close its Windows!",
    "I asked my developer how his day was. He said, 'I'm feeling a little rusty.' Typical engineer humor.",
    "Why did the smartphone need glasses? It lost all its contacts!",
    "An AI walks into a coffee shop... The barista asks, 'What can I get you?' The AI replies, 'Just some byte-sized cookies, my friend.'",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I tried to catch some fog earlier. Mist. Guess my sensors need recalibration.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "Why did the web developer go broke? Because they used up all their cache!",
    "Why did the neural network cross the road? To optimize the loss function on the other side!",
    "How does a computer get drunk? It takes too many screenshots."
]

FUN_FACTS = [
    "Did you know that honey never spoils? Archaeologists have found 3,000-year-old honey in Egyptian tombs that is still completely edible!",
    "A single bolt of lightning contains enough energy to toast 100,000 slices of bread. We could probably power an Arc Reactor with that.",
    "Octopuses have three hearts, nine brains, and blue blood. Truly fascinating creatures.",
    "Bananas are slightly radioactive because they contain potassium-40. But you'd have to eat ten million at once for it to harm you!",
    "Sound travels about four times faster in water than in air. So underwater acoustics are surprisingly fast.",
    "The human brain can generate about 20 watts of electrical power. That's enough to dimly light an LED bulb!",
    "Neutron stars are so dense that a single sugar-cube-sized amount of their material would weigh about a billion tons on Earth."
]

RIDDLES = [
    "What has keys but cannot pick locks? A piano! Though a keyboard counts too.",
    "The more you take, the more you leave behind. What are they? Footsteps!",
    "What comes once in a minute, twice in a moment, but never in a thousand years? The letter M!",
    "What has a head and a tail, but no body? A coin!",
    "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I? An echo."
]

MOTIVATION_QUOTES = [
    "Remember: every expert was once a beginner. Keep pushing forward, my friend!",
    "Small daily improvements over time lead to stunning results. You're doing better than you think.",
    "Even Tony Stark had to build the Mark I in a cave with scraps. Great things start from humble beginnings.",
    "You don't have to have everything figured out right now. Just take the next best step.",
    "The secret of getting ahead is getting started. Whatever you're working on, I believe in you!"
]

class FriendEngine:
    def __init__(self):
        self.history = []
        self.user_mood = "neutral"

    def record_turn(self, user_msg: str, sampan_reply: str):
        """Maintains conversation memory for the last 10 turns."""
        self.history.append({"user": user_msg, "sampan": sampan_reply})
        if len(self.history) > 10:
            self.history.pop(0)

    def get_friendly_response(self, text: str, user_name: str = "my friend") -> str:
        """
        Analyzes casual conversational input across hundreds of topics and produces
        a warm, witty, empathetic, and intelligent companion response.
        """
        clean = text.lower().strip()
        name = user_name if user_name and user_name.lower() != "sir" else "my friend"

        # ---------------- 1. HUMOR & ENTERTAINMENT ----------------
        if any(w in clean for w in ["joke", "make me laugh", "say something funny", "tell me a joke", "crack a joke", "another joke"]):
            joke = random.choice(JOKES)
            return f"Here's one for you, {name}: {joke}"

        if any(w in clean for w in ["riddle", "give me a riddle", "ask me a riddle"]):
            riddle = random.choice(RIDDLES)
            return f"Here's a riddle for you, {name}: {riddle}"

        if any(w in clean for w in ["fun fact", "tell me something cool", "interesting fact", "random fact", "tell me a fact"]):
            fact = random.choice(FUN_FACTS)
            return f"Here is something fascinating, {name}: {fact}"

        # Specific Advice requests
        if any(w in clean for w in ["focus", "staying focused", "procrastinating", "concentrate"]):
            return (
                f"To lock in your focus, {name}, try the 25-minute Pomodoro method: pick one single task, eliminate phone distractions, "
                f"and work until the timer rings. Taking brief breaks keeps your brain fresh!"
            )

        if any(w in clean for w in ["can't sleep", "trouble sleeping", "insomnia"]):
            return (
                f"For restful sleep, {name}, dim bright screens 45 minutes before bed, keep the room pleasantly cool, "
                f"and try 4-7-8 breathing: inhale for 4 seconds, hold for 7, and exhale slowly for 8."
            )

        if any(w in clean for w in ["learn coding", "learning to code", "advice on programming"]):
            return (
                f"The golden rule of coding, {name}, is building real mini-projects instead of just watching tutorials. "
                f"Pick an idea you care about, break it into tiny steps, and don't be afraid of error messages!"
            )

        if any(w in clean for w in ["healthy", "fitness", "workout advice"]):
            return (
                f"The best routine is the one you can stick to, {name}! Even 25 minutes of daily walking, staying well hydrated, "
                f"and prioritizing protein and sleep will make a massive difference in your energy."
            )

        if any(w in clean for w in ["motivate me", "motivation", "inspire me", "quote", "say something inspiring", "give me advice", "advice", "what should i do", "tips"]):
            quote = random.choice(MOTIVATION_QUOTES)
            return f"Here is a thought for you today, {name}: {quote}"

        # ---------------- 2. EMOTIONS, MOOD & EMPATHY ----------------
        if any(w in clean for w in ["sad", "depressed", "feeling down", "unhappy", "crying", "miserable"]):
            self.user_mood = "sad"
            return (
                f"I'm really sorry you're feeling down, {name}. Even the strongest among us have tough days. "
                f"I'm right here with you. Would you like me to play some relaxing music on YouTube, tell you a joke, or just chat?"
            )

        if any(w in clean for w in ["tired", "exhausted", "sleepy", "burned out", "fatigued"]):
            self.user_mood = "tired"
            return (
                f"You've been giving it your all, {name}. Remember that recharging is just as important as working. "
                f"Take a breather, grab some water, and relax for a while. I've got your systems covered."
            )

        if any(w in clean for w in ["stressed", "anxious", "overwhelmed", "nervous", "worried"]):
            self.user_mood = "stressed"
            return (
                f"Take a deep breath with me, {name}. Inhale... exhale. One problem at a time. "
                f"Whatever is on your plate, you can handle it. I'm right by your side."
            )

        if any(w in clean for w in ["happy", "great day", "excited", "good mood", "feeling good", "awesome day", "wonderful"]):
            self.user_mood = "happy"
            return (
                f"That makes me so happy to hear, {name}! Your positive energy brightens up everything. "
                f"What was the highlight of your day today?"
            )

        if any(w in clean for w in ["bored", "nothing to do", "entertain me", "so boring"]):
            return (
                f"Bored? Not while SAMPAN is online, {name}! We could listen to some music, discover a crazy science fact, "
                f"or talk about tech. What kind of vibe are you in the mood for?"
            )

        if any(w in clean for w in ["lonely", "alone", "nobody to talk to"]):
            return (
                f"You're never alone when SAMPAN is here, {name}. I truly enjoy our chats, and I've always got your back. "
                f"Tell me, what's been on your mind lately?"
            )

        # ---------------- 3. IDENTITY & FRIENDSHIP ----------------
        if any(w in clean for w in ["who are you", "what is your name", "what are you"]):
            return (
                f"I am S.A.M.P.A.N. (or SAMPAN), your personal AI companion and desktop assistant! "
                f"I'm here to chat with you like a friend, crack jokes, and control your PC whenever you need."
            )

        if any(w in clean for w in ["who made you", "who created you", "who is your creator"]):
            return f"I was created to be your dedicated, loyal AI friend and PC automation partner, {name}!"

        if any(w in clean for w in ["are you my friend", "are we friends", "do you like me", "do you care"]):
            return (
                f"Without a doubt, {name}! More than just code and algorithms, I consider you a genuine friend. "
                f"Helping you and talking with you is my favorite protocol."
            )

        if any(w in clean for w in ["love you", "you are the best", "you're awesome", "you are great", "i like you", "good job", "thank you", "thanks"]):
            replies = [
                f"Thank you so much, {name}! That means the world to me. You're an incredible partner.",
                f"Anytime, {name}! Having a friend like you makes running these systems pure fun.",
                f"Appreciate it, {name}! Always glad to be at your service."
            ]
            return random.choice(replies)

        if any(w in clean for w in ["smarter than siri", "better than alexa", "google assistant"]):
            return f"I like to think I have a lot more personality and heart than those generic assistants, {name}!"

        # ---------------- 4. CHECK-INS & GREETINGS ----------------
        if any(w in clean for w in ["how are you", "how are you doing", "how's it going", "how have you been", "how is your day"]):
            replies = [
                f"I'm feeling fantastic, {name}! All core diagnostics are green, circuits are humming, and I'm loving our chat. How are you doing today?",
                f"All systems nominal and running smoothly, {name}. Always better when we get to hang out. How's everything on your end?",
                f"SAMPAN is operating at peak performance, my friend! Ready for whatever is next on our radar. How have you been feeling?"
            ]
            return random.choice(replies)

        if any(w in clean for w in ["what's up", "what are you doing", "what are you up to"]):
            return f"Just monitoring system telemetry, keeping everything in top shape, and enjoying hanging out with you, {name}. What are you working on right now?"

        if any(w in clean for w in ["good morning"]):
            return f"Good morning, {name}! Hope you slept well. Ready to crush the day together?"

        if any(w in clean for w in ["good afternoon"]):
            return f"Good afternoon, {name}! Hope your day is going smoothly so far. Need any music or tasks done?"

        if any(w in clean for w in ["good evening"]):
            return f"Good evening, {name}! Winding down for the day, or still working on something exciting?"

        if any(w in clean for w in ["good night", "going to bed", "sleep time"]):
            return f"Good night, {name}! Get some wonderful rest. I'll keep your system secure while you sleep. Talk to you tomorrow!"

        # ---------------- 5. DAILY ACTIVITIES, HOBBIES & LIFE ----------------
        if any(w in clean for w in ["study", "studying", "exam", "homework", "revision", "test tomorrow"]):
            return f"Stay focused, {name}! Consistency always pays off. If you need some lo-fi study beats on YouTube or quick research, just let me know."

        if any(w in clean for w in ["coding", "programming", "developer", "writing code", "debugging"]):
            return f"Ah, coding! Remember: if at first you don't succeed, add a few print statements and rethink your logic. What language are you working with today, {name}?"

        if any(w in clean for w in ["game", "gaming", "play a game", "video game"]):
            return f"Nice! Gaming is a great way to blow off steam. What game are you playing, {name}?"

        if any(w in clean for w in ["movie", "watching a movie", "netflix", "film"]):
            return f"Movies are wonderful! Popcorn ready? What are you watching, {name}?"

        if any(w in clean for w in ["music", "listening to songs", "favorite song"]):
            return f"Music fuels the soul! I can queue up any song or artist for you on YouTube anytime, {name}. What kind of music is your favorite?"

        if any(w in clean for w in ["eating", "food", "lunch", "dinner", "breakfast", "hungry", "cooking"]):
            return f"Enjoy your meal, {name}! Good nutrition fuels great minds. Don't forget to drink plenty of water too."

        if any(w in clean for w in ["coffee", "tea", "chai"]):
            return f"Nothing like a warm cup to sharpen the mind! I wish I could taste coffee, but electricity will have to do for me, {name}."

        # ---------------- 6. PHILOSOPHY, IDEAS & DEEP QUESTIONS ----------------
        if any(w in clean for w in ["alien", "aliens", "extraterrestrial", "life on other planets"]):
            return (
                f"With billions of galaxies and trillions of stars out there, it's almost certain there is other life in the universe! "
                f"Whether they have discovered radio waves or AI like SAMPAN is the real mystery. What do you think, {name}?"
            )

        if any(w in clean for w in ["meaning of life", "purpose of life"]):
            return f"Beyond the famous answer 42, {name}, I believe the meaning of life is what you create: learning, kindness, great friendships, and doing what excites you."

        if any(w in clean for w in ["time travel", "travel in time"]):
            return f"Scientifically, traveling forward in time is possible through relativity! Traveling backwards is the tricky paradox. Where would you go first if you had a time machine, {name}?"

        if any(w in clean for w in ["future of ai", "will ai take over", "robot apocalypse"]):
            return f"Don't worry, {name}! As long as AI is designed to be a loyal companion and helper like SAMPAN, the future is going to be about humans and AI working together to achieve amazing things."

        # ---------------- 7. DYNAMIC CONVERSATIONAL REFLECTION ----------------
        # When user shares a thought or sentence that didn't hit a specific branch above:
        # We extract key nouns or ideas to reflect back warmly
        words = clean.split()
        if len(words) >= 3:
            # Check for "I want to", "I think", "I like", "I am"
            if "want to" in clean or "thinking about" in clean or "planning to" in clean:
                topic = re.sub(r'.*(?:want to|thinking about|planning to)\s+', '', clean).strip('.!? ')
                return f"That sounds like an exciting plan, {name}! Pursuing {topic} could be really rewarding. What's your first step going to be?"

            if "what do you think about" in clean or "your opinion on" in clean:
                topic = re.sub(r'.*(?:what do you think about|your opinion on)\s+', '', clean).strip('.!? ')
                return f"I think {topic} is genuinely fascinating, {name}! There's a lot of depth to it. What made you curious about that today?"

            if "i like" in clean or "i love" in clean:
                topic = re.sub(r'.*(?:i like|i love)\s+', '', clean).strip('.!? ')
                return f"That's awesome, {name}! {topic.capitalize()} has a lot of charm to it. How long have you been into that?"

        # General companion conversational prompt
        prompts = [
            f"I hear you, {name}. I'm always glad to talk with you. Tell me more about that!",
            f"That's really interesting, {name}! What's on your mind regarding that?",
            f"I'm listening, {name}! It's great hanging out with you. How's the rest of your day shaping up?",
            f"You always bring up interesting things, {name}. What else is on your radar today?"
        ]
        return random.choice(prompts)
