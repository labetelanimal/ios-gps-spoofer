@echo off
title iOS GPS Spoofer
echo.
echo  =========================================
echo   iOS GPS Spoofer - Lancement Automatique
echo  =========================================
echo.

:: 1. Verifie si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH !
    echo Rends-toi sur https://www.python.org/downloads/ pour l'installer.
    echo N'oublie pas de cocher la case "Add Python to PATH" lors de l'installation !
    echo.
    pause
    exit /b
)

:: 2. Installe automatiquement les librairies manquantes en mode silencieux (-q)
echo [INFO] Verification et installation des librairies necessaires...
pip install -q -r "%~dp0requirements.txt"

:: 3. Lance l'application
echo [INFO] Lancement de l'application...
python "%~dp0ios_gps_spoofer.py"

pause