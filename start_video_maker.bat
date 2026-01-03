@echo off
REM Inicia la aplicación Video Maker usando el Python del venv
pushd "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "%~dp0main.py"
) else (
    echo No se encontró el entorno virtual .venv. Ejecutando con el Python del sistema...
    python "%~dp0main.py"
)
pause
popd
