@ECHO off
REM Compile from Python to C
CD "Python to C"
CALL compile.bat
REM Copy the resulting C file to "ID3Automator/Compilation/C to exe (Windows)"
COPY ID3Automator.c ..
CD ..
MOVE ID3Automator.c "C to exe (Windows)"
CD "C to exe (Windows)"
REM Compile from C to exe (Windows)
CALL compile.bat
REM Copy the resulting exe file to "ID3Automator/Release"
COPY ID3Automator.exe ..
CD ..
MOVE ID3Automator.exe ..
CD ..
MOVE "ID3Automator.exe" "Release"
REM Return to the "ID3Automator/Compilation"
CD "Compilation"
