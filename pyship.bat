rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q app
rmdir /S /Q installers
call venv\Scripts\activate.bat
REM build this app into a distribution
python -m flit build
REM ship it using AWS default profile
python -m pyship -p default
REM
deactivate
