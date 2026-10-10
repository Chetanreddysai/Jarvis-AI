# J.A.R.V.I.S. // Stark Industries Mark VII OS
### Real-Time Voice-Controlled Autonomous Desktop Assistant

Inspired directly by the Marvel Iron Man movies, this is a real-time, voice-activated desktop application built to give you genuine Stark-level PC automation.

---

## ⚡ Key Highlights & Architecture

1. **Movie-Authentic Voice Engine:**
   - Powered by neural British voice synthesis (`en-GB-RyanNeural`) matching Paul Bettany's J.A.R.V.I.S. from Iron Man.
   - Offline fallback using Windows SAPI / SpeechSynthesizer.

2. **Dedicated Stark Industries Holographic HUD:**
   - **Interactive Arc Reactor:** Central power core with rotating concentric rings, dashed dials, and glowing reactor pulse.
   - **True Power Toggle (Online / Standby):** Click the Arc Reactor or the Power button to turn JARVIS ON or OFF.
     - When **ON (Active)**: Glows electric cyan, monitors voice in real time, executes commands.
     - When **OFF (Standby)**: Arc Reactor dims to warm standby amber, microphones and command processing completely power down to save resources.
   - **Live Audio Visualizer:** Dynamic frequency wave expanding in 360 degrees around the Arc Reactor in real-time when JARVIS speaks or hears your voice.
   - **Real-Time Telemetry Gauges:** Live CPU utilization, RAM usage, storage capacity, and battery cell levels with animated radar scanning.
   - **Transmission Log:** Chronological transcript of user speech and JARVIS actions.

3. **Complete Windows Automation Suite:**
   - **Applications:** "Jarvis, open Chrome", "open Notepad", "open VS Code", "open Spotify", "open Calculator", "close Chrome", etc.
   - **Audio & Media:** "Volume up", "volume down", "mute audio", "pause music", "next track", "previous track".
   - **Screen & Display:** "Take a screenshot", "minimize all windows" (show desktop), "lock workstation".
   - **Web & Media:** "Search Google for [topic]", "Play [song] on YouTube", "Open [website]".
   - **System Telemetry:** "Jarvis, status report", "Jarvis, what time is it?", "what is today's date?".
   - **AI Brain & Knowledge:** Built-in Wikipedia & general knowledge intelligence, with optional 1-click Google Gemini API key support for open-ended conversation and coding help.

---

## 🚀 How to Launch JARVIS

### Method 1: One-Click Desktop Launch (Recommended)
Simply double-click:
```
run_jarvis.bat
```
*(Located in `C:\Users\annar\.gemini\antigravity\scratch\jarvis-ai\run_jarvis.bat`)*

This launches JARVIS in a borderless, dedicated Stark HUD application window.

### Method 2: Command Line
```powershell
cd C:\Users\annar\.gemini\antigravity\scratch\jarvis-ai
python run_jarvis.py
```

---

## 🎙️ Spoken Voice Commands

| Category | Voice Commands Examples | Action |
| :--- | :--- | :--- |
| **Power Toggle** | Click the central Arc Reactor | Toggles between **ONLINE** and **STANDBY** |
| **System Status** | *"Jarvis, status report"* or *"Jarvis, system status"* | Reads out CPU %, RAM used, battery level & time |
| **Launch Apps** | *"Jarvis, open Chrome"* / *"open Notepad"* / *"open Spotify"* | Launches the requested Windows program |
| **Close Apps** | *"Jarvis, close Chrome"* / *"terminate Notepad"* | Exits the target program |
| **Audio Volume** | *"Jarvis, volume up"* / *"volume down"* / *"mute"* | Adjusts master system audio level |
| **Media Playback** | *"Jarvis, pause music"* / *"next track"* / *"previous track"* | Controls background music and videos |
| **Screenshots** | *"Jarvis, take a screenshot"* | Captures screen to `screenshots/` directory |
| **Windows OS** | *"Jarvis, minimize all"* / *"lock computer"* | Minimizes all windows or locks workstation |
| **Web & YouTube** | *"Jarvis, play AC/DC on YouTube"* / *"search Google for [query]"* | Plays media on YouTube or searches Google |
| **Time & Date** | *"Jarvis, what time is it?"* / *"what is today's date?"* | Speaks current time and date |
| **Knowledge** | *"Jarvis, who is Nikola Tesla?"* / *"what is quantum computing?"* | Summarizes information using knowledge engine |

---

## ⚙️ Settings & Gemini API (Optional)
Click the **⚙ SETTINGS** button on the bottom right of the HUD to:
- Enter your **Google Gemini API Key** for conversational AI reasoning.
- Adjust **Voice Speed** (-10%, standard, +10%).
- Change your **Callsign** (default: "Sir").
