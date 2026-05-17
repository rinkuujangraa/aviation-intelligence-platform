@echo off
REM Switch Git Account from theelectron404-blip to rinkuujangraa

echo ========================================
echo Switching Git Account
echo ========================================
echo.

REM Remove old credentials
git config --global --unset credential.helper
git config --global --unset user.name
git config --global --unset user.email

REM Set new account
echo Setting new Git account: rinkuujangraa
git config --global user.name "Rinku"
git config --global user.email "your.email@gmail.com"

REM Use Windows Credential Manager
git config --global credential.helper manager-core

echo.
echo ========================================
echo Git account switched successfully!
echo ========================================
echo.
echo Current configuration:
git config --global user.name
git config --global user.email
echo.
echo Next: When you push, Windows will prompt for GitHub login
echo Use your rinkuujangraa account!
echo.
pause
