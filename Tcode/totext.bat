@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================
REM  Copy all .py files (recursive) into a dated subfolder,
REM  preserving folder structure, and rename to .txt
REM ===========================

REM Folder where this BAT lives (use that as root)
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"

REM Get today's date as YYYY-MM-DD (reliable across locales)
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "TODAY=%%i"

REM Output folder: _pycode_YYYY-MM-DD
set "OUT=%ROOT%\_pycode_%TODAY%"

if not exist "%OUT%" mkdir "%OUT%"

echo Copying .py files under:
echo   %ROOT%
echo To:
echo   %OUT%
echo.

REM Walk all .py files under ROOT
for /r "%ROOT%" %%F in (*.py) do (
  set "SRC=%%F"

  REM Skip anything already inside output folder (prevents re-copy loops)
  echo "!SRC!" | findstr /i /c:"\_pycode_" >nul && (
    REM skip
  ) || (
    REM Make path relative to ROOT
    set "REL=!SRC:%ROOT%\=!"

    REM Compute destination folder (preserve structure)
    for %%D in ("%OUT%\!REL!") do (
      if not exist "%%~dpD" mkdir "%%~dpD" >nul 2>&1
    )

    REM Destination filename: same as source but .txt
    set "DEST=%OUT%\!REL!"
    set "DEST=!DEST:~0,-3!.txt"

    copy /y "%%F" "!DEST!" >nul
    echo Copied: !REL!  -->  !DEST:%OUT%\=!
  )
)

echo.
echo Done.
echo Output folder:
echo   %OUT%
pause
