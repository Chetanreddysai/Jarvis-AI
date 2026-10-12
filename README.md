# S.A.M.P.A.N. // Autonomous AI Desktop Companion & OS
### Real-Time Voice-Controlled Friend & Autonomous PC Assistant

S.A.M.P.A.N. is an interactive, voice-activated AI companion and desktop controller designed to understand anything you say, converse like a trusted friend, answer questions, solve math, check live weather, and carry out full Windows PC automation.

---

## ⚡ Key Highlights & Architecture

1. **Pure Background Voice Assistant (Zero Webpage / Browser Overhead):**
   - **Silent Background Execution**: Runs directly as a background service via `run_background.py`. No browser window, no HUD webpage, and no desktop clutter.
   - **Direct Speaker Audio Playback**: High-fidelity neural voice synthesis (`voice_engine.speak()`) plays directly through your laptop's physical speakers using `pygame.mixer` with automatic microphone feedback suppression.

2. **Universal Open-Ended Conversation & Companionship:**
   - **Understands Any Topic**: Talk freely about your day, thoughts, feelings, philosophy, hobbies, movies, coding, or life advice.
   - **Emotional Empathy & Humor**: Tells witty jokes, mind-blowing facts, riddles, gives genuine encouragement, and supports you when tired or stressed.
   - **Multi-Turn Memory**: Remembers recent conversational context for natural back-and-forth dialogue.

3. **Universal Live Knowledge & Intelligence (Zero API Key Needed):**
   - **Live Internet Information Retrieval**: Searches DuckDuckGo (Lite & HTML) and Wikipedia in real time to answer any questions about current events, people, science, history, geography, sports, winners, concepts, and definitions.
   - **Mathematics & Calculation**: Solves mental math, percentages, square roots, and arithmetic instantly.
   - **Live Weather**: Instant real-time weather and temperature for any city worldwide via wttr.in.
   - **Optional Google Gemini LLM**: Enter a free Google Gemini API key in `config.json` for unlimited generative AI reasoning.

4. **Complete Windows Automation Suite:**
   - **Applications:** "Open Chrome", "launch Notepad", "start Spotify", "open Calculator", "close Chrome", etc.
   - **Audio & Media:** "Volume up", "volume down", "make it louder", "mute audio", "pause music", "next track", "previous track".
   - **Screen & Display:** "Take a screenshot", "minimize all windows", "lock workstation".
   - **Web & YouTube:** "Play [song / artist] on YouTube", "search Google for [query]".
   - **System Telemetry:** "Status report", "battery level", "what time is it?", "what is today's date?".

---

## 🚀 How to Control SAMPAN

### 1. Starting SAMPAN:
Simply double-click:
👉 **`START SAMPAN`** *(on your Desktop)* or **`START_SAMPAN.bat`**

- Runs silently in the background (no browser or webpage opens).
- Listens to your laptop microphone continuously.
- Speaks answers directly through your laptop speakers!

### 2. Stopping SAMPAN:
Whenever you want to stop SAMPAN completely:
👉 **`STOP SAMPAN`** *(on your Desktop)* or **`STOP_SAMPAN.bat`**

- Shuts down all background listeners, microphone recording, and processes.
- Gives a friendly spoken farewell: *"SAMPAN is powered down. Goodbye, my friend."*
- Releases all audio hardware and accepts no further commands.

---

## 🎙️ Spoken Voice Commands & Conversations

| Category | Example Voice Inputs | Action / Response |
| :--- | :--- | :--- |
| **Learning & Memory** | *"My name is Chetan"* / *"Remember that my exam is tomorrow"* / *"What do you remember?"* | Learns user profile, saves reminders, and recaps personal memory permanently |
| **Custom Skill Learning** | *"When I say work, open Chrome and Teams"* | Learns custom multi-action command aliases and executes on cue |
| **Open-Ended Chit-Chat** | *"How are you doing buddy?"* / *"Tell me a joke"* / *"Tell me a riddle"* | Warm, witty banter, humor, riddles, and daily check-ins |
| **Feelings & Empathy** | *"I'm feeling so exhausted"* / *"I had a great day"* / *"I'm stressed"* | Empathetic support, active listening, and uplifting tips |
| **Life Advice & Focus** | *"Give me advice on staying focused"* / *"Can't sleep"* / *"Motivate me"* | Actionable advice (e.g. Pomodoro, 4-7-8 breathing, coding tips) |
| **General Knowledge** | *"Who is the Prime Minister of India?"* / *"National song of India"* / *"Why do birds migrate?"* | Searches live Wikipedia & DuckDuckGo with polished conversational speech |
| **Math & Calculation** | *"What is 75 times 8?"* / *"Calculate 20 percent of 500"* / *"Square root of 144"* | Evaluates expressions and speaks the exact mathematical answer |
| **Live Weather** | *"Weather in Mumbai"* / *"Temperature in London"* / *"Weather today"* | Real-time live temperature and weather condition report |
| **Philosophical Thoughts** | *"Do you believe in aliens?"* / *"What is the meaning of life?"* | Engaging, thoughtful companion opinions on deep questions |
| **Launch Apps & Web** | *"Open Chrome"* / *"open teams in Chrome"* / *"edge"* / *"open Word"* | Launches Windows apps and opens web services in targeted browser |
| **Typing & Dictation** | *"Type hello at the rate gmail.com"* / *"press enter"* | Types dictated text or presses keys in active window |
| **Close Apps** | *"Close Chrome"* / *"terminate Notepad"* | Closes the requested application |
| **Audio Volume** | *"Volume up"* / *"volume down"* / *"make it louder"* / *"mute"* | Adjusts master system audio level |
| **Media Playback** | *"Pause music"* / *"next track"* / *"previous track"* | Controls background music and videos |
| **Screenshots** | *"Take a screenshot"* / *"capture screen"* | Captures screen to `screenshots/` directory |
| **Windows OS** | *"Minimize all"* / *"lock computer"* | Minimizes all windows or locks workstation |
| **YouTube & Web** | *"Play songs on YouTube"* / *"search Google for [query]"* | Plays media on YouTube or searches Google |
| **Time & Date** | *"What time is it?"* / *"what is today's date?"* | Speaks current time and date |
| **System Status** | *"Status report"* / *"battery percentage"* | Reads CPU %, RAM used, battery level & time |

---

## ⚙️ Settings & Gemini API (Optional)
Click the **⚙ SETTINGS** button on the bottom right of the HUD to:
- Enter a **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/)) for unlimited generative AI capability.
- Adjust **Voice Speed** (-10%, standard, +10%).
- Change your **Callsign / Name** (default: "my friend").
