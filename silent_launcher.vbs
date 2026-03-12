' Wait 10 seconds to allow Windows to load Microphone drivers and Mount drives
WScript.Sleep 10000

Set WshShell = CreateObject("WScript.Shell")
' Run the batch file silently
WshShell.Run chr(34) & "e:\projects\My Wispr flow\start_flowtype.bat" & chr(34), 0
Set WshShell = Nothing
