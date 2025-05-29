@echo off
set DEV_THIRD_PARTIES_ROOT_PATH=%~dp0
SETLOCAL
call %DEV_THIRD_PARTIES_ROOT_PATH%\conan\install.windows.bat
ENDLOCAL

