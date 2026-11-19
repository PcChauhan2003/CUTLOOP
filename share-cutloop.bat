@echo off
title CUTLOOP - Live Public Share Tunnel
echo ===================================================
echo     CUTLOOP - Share Live Website With Testers
echo ===================================================
echo.
echo Starting Public Cloudflare Tunnel to port 3000...
cloudflared.exe tunnel --url http://127.0.0.1:3000
pause
