@echo off
chcp 65001 >nul
echo ===================================================
echo   Cập nhật Dữ liệu Tổ Chức ^& Đẩy lên GitHub
echo ===================================================

cd /d "%~dp0"

:: Cố định thư mục nguồn chứa file NN_TD
set "SOURCE_FILE=D:\Dulieuxuatra\NN_TD.csv"
set "TARGET_FILE=data\NN_TD.csv"

echo.
echo [*] Buoc 1: Dong bo du lieu tu %SOURCE_FILE%...
if exist "%SOURCE_FILE%" (
    copy /Y "%SOURCE_FILE%" "%TARGET_FILE%" >nul
    echo [+] Da copy thanh cong sang %TARGET_FILE%
) else (
    echo [!] Khong tim thay file nguon tai %SOURCE_FILE%.
    echo [!] Se su dung du lieu hien tai trong thu muc data.
)

echo.
echo.
echo [*] Buoc 2: Xu ly du lieu va tao bao cao HTML...
C:\Users\ducnx\.venv\Scripts\python.exe main.py
C:\Users\ducnx\.venv\Scripts\python.exe ..\update_news.py
C:\Users\ducnx\.venv\Scripts\python.exe ..\generate_market_dashboard.py
C:\Users\ducnx\.venv\Scripts\python.exe ..\generate_advanced_charts.py

echo.
echo [*] Buoc 2.1: Dong bo file tu thu muc goc vao repo...
copy /Y "..\index.html" "index.html" >nul
copy /Y "..\market_dashboard.html" "market_dashboard.html" >nul
copy /Y "..\institutional_report.html" "institutional_report.html" >nul
copy /Y "..\industry_report.html" "industry_report.html" >nul
copy /Y "..\industry_dashboard.html" "industry_dashboard.html" >nul
if not exist "NEWS" mkdir "NEWS"
xcopy /Y /E /I "..\NEWS\*" "NEWS\" >nul
echo [+] Da dong bo file thanh cong.

echo.
echo [*] Buoc 3: Day du lieu len GitHub...
git add .

:: Lay ngay gio hien tai
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set mydate=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%
set mytime=%datetime:~8,2%:%datetime:~10,2%

git commit -m "Auto-update data and report at %mydate% %mytime%"
git push origin main

echo.
echo [*] Buoc 4: Day du lieu CHISONGANH len GitHub rieng...
set "CHISONGANH_SOURCE=D:\Dulieuxuatra\CHISONGANH.csv"
set "CHISONGANH_REPO=D:\Vibecoding\ND-CHISONGANH"

if exist "%CHISONGANH_SOURCE%" (
    if exist "%CHISONGANH_REPO%" (
        copy /Y "%CHISONGANH_SOURCE%" "%CHISONGANH_REPO%\" >nul
        cd /d "%CHISONGANH_REPO%"
        git add CHISONGANH.csv
        git commit -m "Auto-update CHISONGANH data at %mydate% %mytime%"
        git push origin main
        cd /d "%~dp0"
        echo [+] Da day thanh cong CHISONGANH len GitHub
    ) else (
        echo [!] Khong tim thay repo tai %CHISONGANH_REPO%
    )
) else (
    echo [!] Khong tim thay file nguon CHISONGANH tai %CHISONGANH_SOURCE%
)

echo.
echo ===================================================
echo [SUCCESS] Toan bo qua trinh cap nhat da hoan tat!
echo ===================================================
pause
