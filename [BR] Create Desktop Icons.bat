@echo off

REM This part is taken from the Koikatu Registry Fixer, see Koikatu Registry Fixer for credits.

COLOR D

IF EXIST "%~dp0InitSettingGameStudioVREN.exe" GOTO doWork
IF EXIST "%~dp0InitSettingEN.exe" GOTO doWork
IF EXIST "%~dp0InitSetting.exe" GOTO doWork
IF EXIST "%~dp0InitSetting English.exe" GOTO doWork

ECHO Error
ECHO.
ECHO Found neither "InitSettingGameStudioVREN.exe", "InitSettingEN.exe" nor "InitSetting.exe" (e.g. "InitSetting.exe" ) in "%~dp0"!
ECHO.
ECHO Please, add the Launcher name on "IF EXIST "%~dp0LAUNCHER NAME" GOTO doWork"

cmd /k

:doWork

REG ADD "HKEY_CURRENT_USER\Software\illusion\koikatu\koikatu" /ve /f
ECHO Koikatu added to Regedit

REG ADD "HKEY_CURRENT_USER\Software\illusion\koikatu\koikatu" /v "INSTALLDIR" /d "%~dp0\" /f
ECHO INSTALLDIR added to Regedit

REM This script is heavily based off Brett Zamirs answer on https://superuser.com/questions/392061/how-to-make-a-shortcut-from-cmd
REM Written for usage with the Koikatsu BetterRepack by ScrewThisNoise.

SETLOCAL ENABLEDELAYEDEXPANSION

((
  echo Dim objShell
  echo Dim strPath
  echo Set objShell = Wscript.CreateObject("Wscript.Shell"^)
  echo strPath = objShell.SpecialFolders("Desktop"^)
  echo wscript.echo strPath
)1>FindDesktop.vbs
FOR /F "usebackq tokens=*" %%r in (`CSCRIPT "FindDesktop.vbs"`) DO SET currentdesktop=%%r
DEL FindDesktop.vbs /f /q
)

REM Shortcut for launcher

SET LinkName=Koikatsu
SET Esc_LinkDest=%currentdesktop%\!LinkName!.lnk
SET Esc_LinkIcon=%cd%\koikatu.ico
SET Esc_LinkTarget=%cd%\InitSetting.exe
SET Esc_RunIn=%cd%
SET cSctVBS=CreateShortcut.vbs
SET LOG=".\%~N0_runtime.log"
((
  echo Set oWS = WScript.CreateObject^("WScript.Shell"^) 
  echo sLinkFile = oWS.ExpandEnvironmentStrings^("!Esc_LinkDest!"^)
  echo Set oLink = oWS.CreateShortcut^(sLinkFile^) 
  echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("!Esc_LinkTarget!"^)
  echo oLink.WorkingDirectory = oWS.ExpandEnvironmentStrings^("!Esc_RunIn!"^)
  echo oLink.IconLocation = oWS.ExpandEnvironmentStrings^("!Esc_LinkIcon!"^)
  echo oLink.Save
)1>!cSctVBS!
cscript //nologo .\!cSctVBS!
DEL !cSctVBS! /f /q
)

REM Shortcut to Scenes folder

SET LinkName=Koikatsu Studio Scenes
SET Esc_LinkDest=%currentdesktop%\!LinkName!.lnk
SET Esc_LinkIcon=%cd%\UserData\Studio\scene\KKStudio.ico
SET Esc_LinkTarget=%cd%\UserData\Studio\scene
SET cSctVBS=CreateShortcut.vbs
SET LOG=".\%~N0_runtime.log"
((
  echo Set oWS = WScript.CreateObject^("WScript.Shell"^) 
  echo sLinkFile = oWS.ExpandEnvironmentStrings^("!Esc_LinkDest!"^)
  echo Set oLink = oWS.CreateShortcut^(sLinkFile^) 
  echo oLink.IconLocation = oWS.ExpandEnvironmentStrings^("!Esc_LinkIcon!"^)
  echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("!Esc_LinkTarget!"^)
  echo oLink.Save
)1>!cSctVBS!
cscript //nologo .\!cSctVBS!
DEL !cSctVBS! /f /q
)

REM Shortcut to Character Card folder

SET LinkName=Koikatsu Character Cards
SET Esc_LinkDest=%%currentdesktop%%\!LinkName!.lnk
SET Esc_LinkIcon=%cd%\UserData\chara\KKCards.ico
SET Esc_LinkTarget=%cd%\UserData\chara
SET cSctVBS=CreateShortcut.vbs
SET LOG=".\%~N0_runtime.log"
((
  echo Set oWS = WScript.CreateObject^("WScript.Shell"^) 
  echo sLinkFile = oWS.ExpandEnvironmentStrings^("!Esc_LinkDest!"^)
  echo Set oLink = oWS.CreateShortcut^(sLinkFile^) 
  echo oLink.IconLocation = oWS.ExpandEnvironmentStrings^("!Esc_LinkIcon!"^)
  echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("!Esc_LinkTarget!"^)
  echo oLink.Save
)1>!cSctVBS!
cscript //nologo .\!cSctVBS!
DEL !cSctVBS! /f /q
)

REM Shortcut to Screenshot folder

SET LinkName=Koikatsu Screenshots
SET Esc_LinkDest=%%currentdesktop%%\!LinkName!.lnk
SET Esc_LinkIcon=%cd%\UserData\cap\KKCap.ico
SET Esc_LinkTarget=%cd%\UserData\cap
SET cSctVBS=CreateShortcut.vbs
SET LOG=".\%~N0_runtime.log"
((
  echo Set oWS = WScript.CreateObject^("WScript.Shell"^) 
  echo sLinkFile = oWS.ExpandEnvironmentStrings^("!Esc_LinkDest!"^)
  echo Set oLink = oWS.CreateShortcut^(sLinkFile^) 
  echo oLink.IconLocation = oWS.ExpandEnvironmentStrings^("!Esc_LinkIcon!"^)
  echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("!Esc_LinkTarget!"^)
  echo oLink.Save
)1>!cSctVBS!
cscript //nologo .\!cSctVBS!
DEL !cSctVBS! /f /q
)