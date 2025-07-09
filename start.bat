@echo off
echo Starting LookingGlass backend and frontend...

REM Open backend (Python FastAPI)
start "LookingGlass Backend" cmd /k "python -m backend"

REM Open frontend (React + Vite)
start "LookingGlass Frontend" cmd /k "cd frontend && npm run dev"

echo Both servers launched. Press any key to exit this window.
pause >nul
