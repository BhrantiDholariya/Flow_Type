@echo off
cd /d "e:\projects\My Wispr flow"

:: Kill any old stuck sessions
taskkill /F /IM python.exe /T >nul 2>&1

:: Log the start time
echo [%date% %time%] FlowType Force Restarted >> startup_debug.log

:: Run the app
"e:\projects\My Wispr flow\venv\Scripts\python.exe" -m src.main >> startup_debug.log 2>&1
