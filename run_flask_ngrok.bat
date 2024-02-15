@echo off

rem Start Flask in the background
start python scraper_code.py

rem Sleep for a few seconds to allow Flask to start
timeout /nobreak /t 5 >nul

rem Start Ngrok
ngrok http --domain=relaxing-safely-leech.ngrok-free.app 5000

