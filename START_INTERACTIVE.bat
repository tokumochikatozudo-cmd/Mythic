@echo off
title MYTHIC - Interactive Pentest (Ollama)
echo.
echo  +-------------------------------------------------+
echo  ^|   M Y T H I C  --  Interactive Mode           ^|
echo  ^|   deepseek-r1-tool-calling:7b  (fits VRAM)    ^|
echo  ^|   qwen3.5:2b parser                           ^|
echo  +-------------------------------------------------+
echo.
echo  TIP: type 'next' to feed tool output
echo  TIP: type 'more' for step-by-step commands
echo  TIP: type 'todo' to see the task tree
echo  TIP: type 'quit' to save and exit
echo.
py -3.12 "C:\UNLISTED\mythic.py" legacy
pause
