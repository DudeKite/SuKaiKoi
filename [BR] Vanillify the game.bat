@echo off
COLOR D

IF EXIST "%~dp0InitSetting.exe" GOTO doWork

cls
ECHO Error
ECHO.
ECHO Can't find Koikatsu in "%~dp0"!
ECHO.
ECHO This file is meant to be used with BetterRepack to turn the repack into a vanilla installation.
ECHO Place this file in the BetterRepack install dir and rerun it.
ECHO.
pause
EXIT /B

:doWork
cls
:startscript
echo.
echo.
ECHO      Welcome to the BetterRepack Vanillafier. (^^_^^)
ECHO      This file is meant to be used with BetterRepack to turn the repack into a vanilla installation.
ECHO      This will NOT affect the UserData folder, so any content there is safe.
ECHO.
ECHO      THIS ACTION IS NON-REVERSABLE!
ECHO.
ECHO      Please choose one of the following options:
echo.
echo.
ECHO      1. Remove only translation, leaving the rest of the mods intact
ECHO      2. Remove all BetterRapack Extras
ECHO      3. Remove VR
ECHO      4. Remove all BetterRepack Extras, mods, translation and VR
ECHO      5. Exit
echo.
echo.
SET /P ACTION="Please choose how you'd like to proceed: "
  cls
2>NUL CALL :CASE_%ACTION% # jump to choosen case
IF ERRORLEVEL 1 CALL :DEFAULT_CASE # If label doesn't exist

ECHO Done.
EXIT /B

:CASE_1
REM Remove translation
  echo.
  echo THIS PART IS OBSOLETE!
  echo ----------------------------------
  echo Please choose japanese language in the launcer.
  goto startscript

:CASE_2
REM Remove BetterRapack Extras
  echo.
  echo THIS WILL REMOVE ALL UTILITIES AND NONESSENTIAL EXTRA STUFF!
  echo ----------------------------------
  echo If you wish to abort, please close this window now!
  echo.
  pause
  rmdir /S /Q "[MODDING] Tools"
  rmdir /S /Q "[OPTIONAL] BRExtras"
  rmdir /S /Q "[OPTIONAL] Mods"
  rmdir /S /Q "[UTILITY] IllusionSorter v1.0"
  rmdir /S /Q "[UTILITY] KKManager"
  rmdir /S /Q "[UTILITY] KoiCatalog"
  rmdir /S /Q "[UTILITY] KoikatuCharaReader"
  cls
  ECHO BetterRepack Extras removed
  goto END_ALL

:CASE_3
REM Remove VR
  echo.
  echo THIS WILL REMOVE ALL VR FUNCTIONALITY!
  echo ----------------------------------
  echo If you wish to abort, please close this window now!
  echo.
  pause
  rmdir /S /Q "manual_v"
  rmdir /S /Q "KoikatuVR_Data"
  rmdir /S /Q "abdata\vr"
  del "KoikatuVR.exe"
  cls
  ECHO VR removed
  goto startscript
  
:CASE_4
REM Full vanilla
  echo.
  echo THIS WILL COMPLETELY REVERT THIS PACK TO A VANILLA STATE!
  echo ----------------------------------
  echo This will not affect you UserData folder, thus not touching your cards or scenes.
  echo If you wish to abort, please close this window now!
  echo.
  pause
  rmdir /S /Q "[OPTIONAL] BRExtras"
  rmdir /S /Q "[OPTIONAL] Mods"
  rmdir /S /Q "[UTILITY] KoiCatalog"
  rmdir /S /Q "[UTILITY] KoikatuCharaReader"
  rmdir /S /Q "BepInEx"
  rmdir /S /Q "mods"
  del "InitSetting EN.exe"
  del "doorstop_config.ini"
  del "winhttp.dll"
  del "version"
  goto END_ALL
  
:CASE_5
  GOTO END
  
:DEFAULT_CASE
  ECHO Unknown choice, please try again.
  GOTO startscript
:END_CASE
  VER > NUL # reset ERRORLEVEL
  
:END_ALL
  del "[BR] *"
  goto END
  
:END
  echo.
  echo.
  ECHO      This concludes this script.
  echo.
  echo.
  ECHO      Thank you for choosing BetterRepack^^!
  ECHO                           -ScrewThisNoise
  echo.
  echo.
  
  pause
  EXIT /B

