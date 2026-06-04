@echo off

echo Attivazione dell'ambiente virtuale... 

call C:\Users\Simone\Desktop\CorsoEthosAvanzato\venv\Scripts\activate.bat

echo Ambiente virtuale attivato. Verifica delle dipendenze...
if not exist "requirements.txt" (
    echo File requirements.txt non trovato. Release bloccata.
    exit /b 1
)

echo Installazione delle dipendenze...
pip install -r requirements.txt



echo Avvio dei test...
pytest

if %errorlevel% neq 0 (
    echo Test falliti. Release bloccata.
    exit /b 1
)

echo Test superati. Il progetto puo essere rilasciato.
pause