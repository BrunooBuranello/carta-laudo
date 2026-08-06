@echo off
title Carta Laudo

call ".venv\Scripts\activate.bat"

python main.py

if errorlevel 1 (
    echo.
    echo ===========================================
    echo O processo terminou com ERRO.
    echo Consulte o arquivo de log.
    echo ===========================================
) else (
    echo.
    echo ===========================================
    echo Processo concluido com sucesso.
    echo ===========================================
)

pause
