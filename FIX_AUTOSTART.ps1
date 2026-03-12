$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\FlowTypeAssistant.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"e:\projects\My Wispr flow\silent_launcher.vbs`""
$Shortcut.WorkingDirectory = "e:\projects\My Wispr flow"
$Shortcut.WindowStyle = 7 # Minimized/Hidden
$Shortcut.Save()

Write-Host "✅ DONE! FlowType is now in your Startup folder." -ForegroundColor Green
Write-Host "I have also cleaned up any old registry entries." -ForegroundColor Cyan

# Cleanup old registry try
Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name "FlowTypeAssistant" -ErrorAction SilentlyContinue

Write-Host "`nYou can now RESTART your laptop. It will work automatically!" -ForegroundColor Green
