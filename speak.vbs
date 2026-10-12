Dim voice, text
If WScript.Arguments.Count > 0 Then
    text = WScript.Arguments(0)
    Set voice = CreateObject("SAPI.SpVoice")
    voice.Speak text
End If
