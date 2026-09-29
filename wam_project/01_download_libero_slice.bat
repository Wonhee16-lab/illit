@echo off
chcp 936 >nul
REM ================================================================
REM  下载 LIBERO 数据集小切片（episodes 0~19，约 750MB）
REM  完整数据集约 12.8GB；改 wam_project\01_download_libero_slice.py 可调整
REM ================================================================
cd /d C:\Users\WonHee\lerobot
set HF_ENDPOINT=https://hf-mirror.com
set HF_HUB_DISABLE_XET=1
.venv\Scripts\python.exe -X utf8 wam_project\01_download_libero_slice.py
echo.
pause
