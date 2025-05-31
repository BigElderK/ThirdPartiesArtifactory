@echo off
set BUILD_ENV_ROOT_PATH=%~dp0
SETLOCAL
call %BUILD_ENV_ROOT_PATH%\conan\dev.install.builder.windows.bat
ENDLOCAL

