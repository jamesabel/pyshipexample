rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q app
rmdir /S /Q installers
call venv\Scripts\activate.bat
python -m flit build
python -m demo
deactivate
