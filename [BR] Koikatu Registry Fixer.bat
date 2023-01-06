@echo off

ECHO This tool was created for Musume 3D by fenris666 and reworked by VTRinNights
ECHO to fix registry errors in Koitaku.
ECHO All thanks go to fenris666 for the code.
ECHO.
IF EXIST "%~dp0InitSettingGameStudioVREN.exe" GOTO doWork
IF EXIST "%~dp0InitSettingEN.exe" GOTO doWork
IF EXIST "%~dp0InitSetting.exe" GOTO doWork

ECHO Error
ECHO.
ECHO Found neither "InitSettingGameStudioVREN.exe", "InitSettingEN.exe" nor "InitSetting.exe" (e.g. "InitSetting.exe" ) in "%~dp0"!
ECHO.
ECHO Please, add the Launcher name on "IF EXIST "%~dp0LAUNCHER NAME" GOTO doWork"

cmd /k

:doWork

REG ADD "HKEY_CURRENT_USER\Software\illusion\koikatu\koikatu" /ve /f
ECHO Koikatu added to registry

REG ADD "HKEY_CURRENT_USER\Software\illusion\koikatu\koikatu" /v "INSTALLDIR" /d "%~dp0\" /f
ECHO INSTALLDIR added to registry

ECHO.
ECHO The path "%~dp0" is now correctly registered.

PAUSE
exit