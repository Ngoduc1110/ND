@echo off
chcp 65001 >nul
echo ===================================================
echo   Cập nhật Dữ liệu Tổ Chức ^& Đẩy lên GitHub
echo ===================================================

cd /d "%~dp0"

echo.
echo [*] Buoc 1: Dong bo du lieu tu local va tao bao cao HTML...
C:\Users\ducnx\.venv\Scripts\python.exe src\updater.py

echo.
echo [*] Buoc 2: Day du lieu len GitHub...
git add .

:: Lay ngay gio hien tai
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set mydate=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%
set mytime=%datetime:~8,2%:%datetime:~10,2%

git commit -m "Auto-update data and report at %mydate% %mytime%"
git push origin main

echo.
echo ===================================================
echo [SUCCESS] Toan bo qua trinh cap nhat da hoan tat!
echo ===================================================
pause
