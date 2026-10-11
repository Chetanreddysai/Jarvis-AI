Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\annar\.gemini\antigravity\scratch\jarvis-ai"
WshShell.Run "pythonw run_gui.py", 0, False
