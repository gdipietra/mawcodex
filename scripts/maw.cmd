@echo off
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%~dp0maw.ps1" %*
exit /b %ERRORLEVEL%
