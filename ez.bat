@echo off
setlocal
set GITHUB_REPO=https://github.com/ken3009le/bumbumcuti.git
set BRANCH=main
git config --global user.name "ken3009le"
git config --global user.email "ken3009le@gmail.com"
git commit --amend --reset-author -m "🔥 Force push full project with large files - Kenzema"
git push --force
where git >nul 2>&1
IF NOT EXIST ".git" (
    echo [+] Initializing Git repo...
    git init
    git remote add origin %GITHUB_REPO%
)
where git-lfs >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Git LFS not found. Cài Git LFS rồi chạy lại.
    pause
    exit /b
)
git lfs install
git lfs track "*.mp4"
git lfs track "*.ts"
git lfs track "*.zip"
git lfs track "*.mov"
git lfs track "*.iso"
echo [+] Đang thêm toàn bộ file (kể cả lớn)...
git add --all -f
git commit -m "🔥 Force push"
git config --global http.postBuffer 524288000
echo [+] Push lên GitHub repo: %GITHUB_REPO%
git push -u origin %BRANCH% --force
echo.
echo [+] DONE. Full force push completed.
pause
endlocal
