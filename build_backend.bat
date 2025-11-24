@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Building Backend Executable...
cd backend
pyinstaller --noconfirm --onefile --windowed --name "interview-backend" main.py

echo.
echo Build complete!
echo Executable is in backend/dist/interview-backend.exe
pause
