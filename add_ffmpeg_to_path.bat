@echo off
chcp 65001 >nul
echo ============================================
echo    AudioCraft Pro — הגדרת FFmpeg ב-PATH
echo ============================================
echo.

:: Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo שגיאה: יש להריץ קובץ זה כ-Administrator
    echo לחץ ימני על הקובץ ובחר "Run as administrator"
    pause
    exit /b 1
)

:: Ask for FFmpeg folder
echo הזן את הנתיב לתיקיית FFmpeg (שמכילה ffmpeg.exe)
echo לדוגמה: C:\ffmpeg\bin
echo.
set /p FFMPEG_PATH="נתיב: "

:: Validate path exists
if not exist "%FFMPEG_PATH%\ffmpeg.exe" (
    echo.
    echo שגיאה: לא נמצא ffmpeg.exe בנתיב שהוזן.
    echo ודא שהנתיב מכיל את ffmpeg.exe ונסה שוב.
    pause
    exit /b 1
)

:: Add to System PATH permanently
for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set CURRENT_PATH=%%B

:: Check if already in PATH
echo %CURRENT_PATH% | find /i "%FFMPEG_PATH%" >nul
if %errorLevel% equ 0 (
    echo.
    echo FFmpeg כבר נמצא ב-PATH. אין צורך בשינוי.
    pause
    exit /b 0
)

:: Add to system PATH
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%CURRENT_PATH%;%FFMPEG_PATH%" /f >nul

if %errorLevel% equ 0 (
    echo.
    echo ✓ FFmpeg נוסף בהצלחה ל-PATH של המערכת!
    echo.
    echo נתיב שנוסף: %FFMPEG_PATH%
    echo.
    echo חשוב: יש לפתוח חלון Command Prompt חדש כדי שהשינוי יכנס לתוקף.
    echo התוכנה AudioCraft Pro תזהה את FFmpeg אוטומטית בהפעלה הבאה.
) else (
    echo.
    echo שגיאה: לא הצלחנו לעדכן את PATH. נסה שוב כ-Administrator.
)

echo.
pause
