@echo off
echo ========================================
echo   QA Coverage Dashboard
echo ========================================
echo.
echo Avvio dashboard...
echo Browser si aprira' automaticamente
echo.
echo Per fermare: Premi CTRL+C
echo ========================================
echo.

.venv\Scripts\streamlit.exe run dashboard.py

pause
