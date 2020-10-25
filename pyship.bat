call venv\Scripts\activate.bat
REM build this app into a distribution
python -m flit build
REM ship it
python -m pyship
REM
deactivate
