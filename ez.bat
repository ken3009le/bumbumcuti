@echo off
setlocal

REM === Config tài khoản và repo ===
set GITHUB_REPO=https://github.com/ken3009le/bumbumcuti.git
set BRANCH=main

REM === Cấu hình git username/email nếu chưa có ===
git config --global user.name "ken3009le"
git config --global user.email "kenzema@spyronx.org"

REM === Init Git repo nếu chưa tồn tại ===
IF NOT EXIST ".git" (
    echo [+] Initializing Git repo...
    git init
    git remote add origin %GITHUB_REPO%
)

REM === Cài Git LFS nếu chưa ===
where git-lfs >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] Git LFS not found. Cài Git LFS rồi chạy lại.
    pause
    exit /b
)
git lfs install

REM === Track các loại file lớn ===
git lfs track "*.mp4"
git lfs track "*.ts"
git lfs track "*.zip"
git lfs track "*.mov"
git lfs track "*.iso"

REM === Add everything forcefully ===
echo [+] Đang thêm toàn bộ file (kể cả lớn)...
git add --all -f

REM === Commit (force) ===
git commit -m "🔥 Force push toàn bộ project với file lớn - Kenzema"

REM === Tăng giới hạn push để tránh lỗi ===
git config --global http.postBuffer 524288000

REM === Force push lên branch ===
echo [+] Push lên GitHub repo: %GITHUB_REPO%
git push -u origin %BRANCH% --force

echo.
echo [+] DONE. Full force push completed.
pause
endlocal
