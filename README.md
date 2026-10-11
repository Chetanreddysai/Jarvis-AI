# S.A.M.P.A.N. // Autonomous AI Desktop Companion & OS
### Real-Time Voice-Controlled Friend & Autonomous PC Assistant

S.A.M.P.A.N. is an interactive, voice-activated AI companion and desktop controller designed to talk with you like a friend, crack jokes, chit-chat, and carry out full Windows PC automation.

---

## ⚡ Key Highlights & Architecture

1. **Conversational Friend & Companion Persona:**
   - Talks with warmth, humor, and empathy like a trusted companion.
   - Tells jokes, shares fun facts, supports you when you are tired or stressed, and answers open-ended chit-chat.
   - Offline conversational engine with optional 1-click Google Gemini AI integration for unlimited depth.

2. **Movie-Authentic Voice Engine:**
   - Powered by neural voice synthesis (`en-GB-RyanNeural`) for clear, crisp responses.
   - Offline fallback using Windows SAPI / SpeechSynthesizer.

3. **Dedicated Holographic Arc Reactor HUD:**
   - **Interactive Arc Reactor:** Central power core with rotating concentric rings, dashed dials, and glowing reactor pulse.
   - **True Power Toggle (Online / Standby):** Click the Arc Reactor or the Power button to turn SAMPAN ON or OFF.
     - When **ON (Active)**: Glows electric cyan, monitors voice in real time, executes commands.
     - When **OFF (Standby)**: Arc Reactor dims to warm standby amber, microphones and command processing completely power down to save resources.
   - **Live Audio Visualizer:** Dynamic frequency wave expanding in 360 degrees around the Arc Reactor in real-time when SAMPAN speaks or hears your voice.
   - **Real-Time Telemetry Gauges:** Live CPU utilization, RAM usage, storage capacity, and battery cell levels with animated radar scanning.
   - **Transmission Log:** Chronological transcript of conversation and SAMPAN actions.

4. **Complete Windows Automation Suite:**
   - **Applications:** "Sampan, open Chrome", "open Notepad", "open VS Code", "open Spotify", "open Calculator", "close Chrome", etc.
   - **Audio & Media:** "Volume up", "volume down", "mute audio", "pause music", "next track", "previous track".
   - **Screen & Display:** "Take a screenshot", "minimize all windows" (show desktop), "lock workstation".
   - **Web & Media:** "Search Google for [topic]", "Play [song] on YouTube", "Open [website]".
   - **System Telemetry:** "Sampan, status report", "Sampan, what time is it?", "what is today's date?".
   - **AI Brain & Knowledge:** Built-in Wikipedia & general knowledge intelligence, with optional 1-click Google Gemini API key support for open-ended conversation and coding help.

---

## 🚀 How to Control SAMPAN

### 1. Starting SAMPAN:
Simply double-click:
👉 **`START_SAMPAN.bat`** *(or the **START SAMPAN** shortcut on your Desktop)*

This launches SAMPAN in its dedicated borderless HUD application window and energizes the voice engine.

### 2. Stopping SAMPAN:
Whenever you want to stop SAMPAN completely:
👉 **`STOP_SAMPAN.bat`** *(or the **STOP SAMPAN** shortcut on your Desktop)*

This immediately terminates all background processes, releases the microphone, and stops listening for any commands.

### Method 2: Command Line
```powershell
cd C:\Users\annar\.gemini\antigravity\scratch\jarvis-ai
python run_sampan.py
```

---

## 🎙️ Spoken Voice Commands

| Category | Voice Commands Examples | Action |
| :--- | :--- | :--- |
| **Friend & Chit-Chat** | *"Sampan, how are you doing buddy?"* / *"Tell me a joke"* / *"I'm feeling tired"* / *"Are you my friend?"* | Talks like a warm, witty best friend, jokes, and chats |
| **Power Toggle** | Click the central Arc Reactor | Toggles between **ONLINE** and **STANDBY** |
| **System Status** | *"Sampan, status report"* or *"Sampan, system status"* | Reads out CPU %, RAM used, battery level & time |
| **Launch Apps** | *"Sampan, open Chrome"* / *"open Notepad"* / *"open Spotify"* | Launches the requested Windows program |
| **Close Apps** | *"Sampan, close Chrome"* / *"terminate Notepad"* | Exits the target program |
| **Audio Volume** | *"Sampan, volume up"* / *"volume down"* / *"mute"* | Adjusts master system audio level |
| **Media Playback** | *"Sampan, pause music"* / *"next track"* / *"previous track"* | Controls background music and videos |
| **Screenshots** | *"Sampan, take a screenshot"* | Captures screen to `screenshots/` directory |
| **Windows OS** | *"Sampan, minimize all"* / *"lock computer"* | Minimizes all windows or locks workstation |
| **Web & YouTube** | *"Sampan, play music on YouTube"* / *"search Google for [query]"* | Plays media on YouTube or searches Google |
| **Time & Date** | *"Sampan, what time is it?"* / *"what is today's date?"* | Speaks current time and date |
| **Knowledge** | *"Sampan, who is Nikola Tesla?"* / *"what is quantum computing?"* | Summarizes information using knowledge engine |

---

## ⚙️ Settings & Gemini API (Optional)
Click the **⚙ SETTINGS** button on the bottom right of the HUD to:
- Enter your **Google Gemini API Key** for conversational AI reasoning.
- Adjust **Voice Speed** (-10%, standard, +10%).
- Change your **Callsign / Name** (default: "my friend").
