@echo off
chcp 65001 >nul
echo Vérification et installation des modules requis...

:: Installe les modules nécessaires
pip install --upgrade pillow beautifulsoup4 discord aiohttp psutil mss requests pycryptodome

:: Exécute main.py
echo Lancement de main.py...
python main.py
if %errorlevel% neq 0 (
    echo "py" a échoué, tentative avec python...
    py main.py
    if %errorlevel% neq 0 (
        echo Impossible de lancer le script avec py ou python.
        pause
        exit /b 1
    )
)