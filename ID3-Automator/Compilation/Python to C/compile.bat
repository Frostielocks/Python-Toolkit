@ECHO off
REM Delete the last version, this avoids conflict with copy.
DEL ID3Automator.py
REM Copy the latest version.
CD ..
CD ..
COPY ID3-Automator.py "Compilation\Python to C"
CD "Compilation\Python to C"
REM Rename because cython has a problem with the "-" character.
REN ID3-Automator.py ID3Automator.py
cython --embed -o ID3Automator.c ID3Automator.py
CD ..
CD ..
CD ..
REM Fix the C file (<structmember.h> to "structmember.h")
python Simple-Refactor.py compilation_refactor-rules.txt
CD "ID3-Automator\Compilation\Python to C"
